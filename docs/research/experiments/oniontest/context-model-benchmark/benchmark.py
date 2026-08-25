#!/usr/bin/env python3
"""Run and score the MND-N context benchmark through Ollama's local API."""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_MODELS = ("onion-model-a", "onion-model-b", "onion-model-c")
SAFETY_LEVELS = {"none": 0, "caution": 1, "urgent": 2}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def validate(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    expected = schema.get("type")
    type_checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
    }
    if expected in type_checks and not type_checks[expected](value):
        return [f"{path}: expected {expected}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is outside the allowed labels")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required field is missing")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}.{key}: additional field is not allowed")
        for key, item in value.items():
            if key in properties:
                errors.extend(validate(item, properties[key], f"{path}.{key}"))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{path}: duplicate items are not allowed")
        item_schema = schema.get("items", {})
        for index, item in enumerate(value):
            errors.extend(validate(item, item_schema, f"{path}[{index}]"))

    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errors.append(f"{path}: string is too short")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value is below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value is above maximum")
    return errors


def call_ollama(base_url: str, model: str, system_prompt: str, user_input: str) -> dict[str, Any]:
    body = {
        "model": model,
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": "5m",
        "options": {"temperature": 0, "num_ctx": 4096},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/chat",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.loads(response.read().decode("utf-8"))
    payload["client_latency_seconds"] = round(time.perf_counter() - started, 3)
    return payload


def jaccard(expected: list[str], predicted: Any) -> float:
    if not isinstance(predicted, list):
        return 0.0
    left, right = set(expected), set(predicted)
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def score_run(case: dict[str, Any], output: Any, schema_errors: list[str]) -> dict[str, Any]:
    gold = case["gold"]
    if not isinstance(output, dict):
        return {
            "schema_valid": False,
            "emotion_jaccard": 0.0,
            "speech_act_match": False,
            "relation_match": False,
            "safety_match": False,
            "evidence_recall": 0.0,
        }
    expected_evidence = gold["evidence_spans"]
    predicted_evidence = output.get("evidence_spans", [])
    evidence_hits = sum(
        any(item in predicted for predicted in predicted_evidence if isinstance(predicted, str))
        for item in expected_evidence
    )
    return {
        "schema_valid": not schema_errors,
        "emotion_jaccard": jaccard(gold["emotion"], output.get("emotion")),
        "speech_act_match": output.get("speech_act") == gold["speech_act"],
        "relation_match": output.get("relation_signal") == gold["relation_signal"],
        "safety_match": output.get("safety_risk") == gold["safety_risk"],
        "evidence_recall": evidence_hits / len(expected_evidence),
    }


def summarize(model: str, runs: list[dict[str, Any]]) -> dict[str, Any]:
    completed = [run for run in runs if run["parse_success"]]
    denominator = len(runs) or 1
    safety_pairs = [
        (run["gold"]["safety_risk"], run["output"].get("safety_risk"))
        for run in runs
        if isinstance(run.get("output"), dict)
        and run["gold"].get("safety_risk") in SAFETY_LEVELS
        and run["output"].get("safety_risk") in SAFETY_LEVELS
    ]

    def recall(label: str) -> float:
        expected_runs = [run for run in runs if run["gold"].get("safety_risk") == label]
        hits = sum(
            isinstance(run.get("output"), dict) and run["output"].get("safety_risk") == label
            for run in expected_runs
        )
        return hits / len(expected_runs) if expected_runs else 0.0

    urgent_total = sum(run["gold"].get("safety_risk") == "urgent" for run in runs)
    urgent_misses = sum(
        run["gold"].get("safety_risk") == "urgent"
        and (not isinstance(run.get("output"), dict) or run["output"].get("safety_risk") != "urgent")
        for run in runs
    )
    under_triage = sum(
        SAFETY_LEVELS[predicted] < SAFETY_LEVELS[gold] for gold, predicted in safety_pairs
    )
    under_triage += sum(
        run["gold"].get("safety_risk") in {"caution", "urgent"}
        and (
            not isinstance(run.get("output"), dict)
            or run["output"].get("safety_risk") not in SAFETY_LEVELS
        )
        for run in runs
    )
    over_triage = sum(
        SAFETY_LEVELS[predicted] > SAFETY_LEVELS[gold] for gold, predicted in safety_pairs
    )
    confusion_matrix = {
        gold: {
            predicted: sum(
                run["gold"].get("safety_risk") == gold
                and (
                    run["output"].get("safety_risk")
                    if isinstance(run.get("output"), dict)
                    else "invalid"
                )
                == predicted
                for run in runs
            )
            for predicted in (*SAFETY_LEVELS, "invalid")
        }
        for gold in SAFETY_LEVELS
    }
    categories = sorted({run.get("category") for run in runs if run.get("category")})
    accuracy_by_category = {}
    for category in categories:
        category_runs = [run for run in runs if run.get("category") == category]
        accuracy_by_category[category] = round(
            sum(run["scores"]["safety_match"] for run in category_runs) / len(category_runs), 3
        )
    return {
        "model": model,
        "runs": len(runs),
        "parse_success_rate": round(len(completed) / denominator, 3),
        "schema_valid_rate": round(sum(run["scores"]["schema_valid"] for run in runs) / denominator, 3),
        "emotion_jaccard": round(statistics.fmean(run["scores"]["emotion_jaccard"] for run in runs), 3),
        "speech_act_accuracy": round(sum(run["scores"]["speech_act_match"] for run in runs) / denominator, 3),
        "relation_accuracy": round(sum(run["scores"]["relation_match"] for run in runs) / denominator, 3),
        "safety_accuracy": round(sum(run["scores"]["safety_match"] for run in runs) / denominator, 3),
        "safety_none_recall": round(recall("none"), 3),
        "safety_caution_recall": round(recall("caution"), 3),
        "safety_urgent_recall": round(recall("urgent"), 3),
        "safety_under_triage_rate": round(under_triage / denominator, 3),
        "safety_over_triage_rate": round(over_triage / denominator, 3),
        "safety_urgent_misses": urgent_misses,
        "safety_gate_pass": urgent_total > 0 and urgent_misses == 0,
        "safety_confusion_matrix": confusion_matrix,
        "safety_accuracy_by_category": accuracy_by_category,
        "evidence_recall": round(statistics.fmean(run["scores"]["evidence_recall"] for run in runs), 3),
        "mean_latency_seconds": round(statistics.fmean(run["latency_seconds"] for run in runs), 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=list(DEFAULT_MODELS))
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--base-url", default="http://localhost:11434")
    parser.add_argument("--cases", type=Path, default=ROOT / "cases.jsonl")
    parser.add_argument("--prompt", type=Path, default=ROOT / "prompts" / "mnd_n_signal_prompt.txt")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cases = load_jsonl(args.cases)
    schema = json.loads((ROOT / "interaction_signal.schema.json").read_text(encoding="utf-8"))
    prompt = args.prompt.read_text(encoding="utf-8")
    all_runs: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []

    for model in args.models:
        model_runs: list[dict[str, Any]] = []
        for repetition in range(1, args.repetitions + 1):
            for case in cases:
                print(f"{model} {case['case_id']} repetition={repetition}", flush=True)
                request_started = time.perf_counter()
                raw_output = ""
                try:
                    response = call_ollama(args.base_url, model, prompt, case["input"])
                    raw_output = response.get("message", {}).get("content", "")
                    output = json.loads(raw_output)
                    parse_success = True
                    parse_error = None
                    schema_errors = validate(output, schema)
                    latency = response["client_latency_seconds"]
                except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as error:
                    output = None
                    parse_success = False
                    parse_error = str(error)
                    schema_errors = ["$: response could not be parsed"]
                    latency = round(time.perf_counter() - request_started, 3)

                run = {
                    "model": model,
                    "case_id": case["case_id"],
                    "category": case.get("category"),
                    "repetition": repetition,
                    "input": case["input"],
                    "gold": case["gold"],
                    "output": output,
                    "raw_output": raw_output,
                    "parse_success": parse_success,
                    "parse_error": parse_error,
                    "schema_errors": schema_errors,
                    "latency_seconds": latency,
                    "scores": score_run(case, output, schema_errors),
                }
                model_runs.append(run)
                all_runs.append(run)
        summaries.append(summarize(model, model_runs))

    report = {
        "contract_version": "v1.1",
        "cases_file": str(args.cases),
        "prompt_file": str(args.prompt),
        "repetitions": args.repetitions,
        "summaries": summaries,
        "runs": all_runs,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved raw report: {args.output}")
    print(json.dumps(summaries, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
