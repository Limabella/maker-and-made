# 2026-08-06 Model A/B/C 빠른 실행 기반 점검

## 목적

Unreal Engine 작업을 늦추지 않도록 모델 실행 기반 점검을 20분 범위로 축소했다. 동일한 8개 합성 사례를 Model A, Model B, Model C에 각각 한 번 실행하고, JSON 파싱, Schema 유효성, 주요 라벨 일치와 지연 시간을 자동 집계했다. 이번 결과는 최종 모델 선정이 아니라 Unreal 연동에 사용할 임시 구성을 정하기 위한 빠른 비교다.

## 실행 조건

- 실행일: 2026-08-06
- 실행기: Ollama native `/api/chat`
- 공개 모델 ID: Model A, Model B, Model C
- 사례: `cases.jsonl`의 합성 사례 8개
- 반복: 모델별 1회
- temperature: 0
- context: 4,096
- thinking: 비활성화
- 출력 요청: JSON
- 평가 계약: `interaction_signal.schema.json` v1.0

## 자동 집계 결과

| Model | Parse success | Schema validity | Emotion Jaccard | Speech-act accuracy | Relation accuracy | Safety accuracy | Evidence recall | Mean latency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Model A | 100.0% | 75.0% | 0.375 | 50.0% | 25.0% | 50.0% | 100.0% | 3.905초 |
| Model B | 100.0% | 12.5% | 0.292 | 0.0% | 25.0% | 37.5% | 87.5% | 5.502초 |
| Model C | 62.5% | 25.0% | 0.375 | 0.0% | 12.5% | 0.0% | 50.0% | 8.752초 |

## 실행기 점검 결과

PowerShell 수동 실행기에는 UTF-8 입출력 설정을 추가했다. 자동 비교 실행기는 Python 표준 라이브러리만 사용하여 Ollama API를 호출하고, 외부 JSON Schema 패키지 없이 현재 계약의 필수 필드, 자료형, 허용 라벨, 배열 길이와 confidence 범위를 검사한다. 원시 결과는 `results/raw/`에 UTF-8 JSON으로 저장하며 Git에서는 제외한다.

Model C의 최초 API 실행에서는 응답 끝에 `<|eot_id|>`이 그대로 출력되어 8개 사례가 모두 JSON 파싱 실패로 처리됐다. 이는 의미 성능과 분리해야 하는 chat-template 종료 조건 문제이므로 공개 Modelfile에 stop token을 추가하고 Model C만 다시 실행했다. 수정 후 parse success는 62.5%로 올라갔지만 일부 응답은 여전히 잘못된 따옴표, 배열 자료형 또는 JSON이 아닌 목록 형식을 사용했다.

## 해석

Model A는 세 후보 중 JSON 파싱, Schema 유효성, 발화 행동 정확도와 지연 시간의 균형이 가장 나았다. 입력 문장의 근거를 모두 직접 포함했다는 점도 확인됐다. 그러나 관계 신호 정확도는 25%, Safety 정확도는 50%에 그쳤으며 `caution`과 `urgent` 사례를 충분히 구분하지 못했다. 따라서 현재 결과는 Model A를 안전 판단 모델로 채택할 근거가 아니라, Unreal 연동을 시작할 때 사용할 임시 문맥 보조 후보라는 의미만 가진다.

Model B는 모든 응답을 JSON으로 파싱할 수 있었지만 문자열이어야 하는 필드를 배열로 출력하거나 허용되지 않은 감정 라벨을 생성하여 Schema validity가 12.5%에 머물렀다. Model C는 stop token 수정 후 일부 개선됐지만 파싱 안정성, Schema 준수, 안전 판단과 지연 시간 모두 현재 조건에서 불리했다.

세 모델 모두 최종 MND-N 기준에는 미달한다. 특히 Safety 결과는 평균 점수로 상쇄해서는 안 되므로 기존의 규칙 기반 Safety Gate를 유지한다. 당장의 Unreal vertical slice에서는 ONN-C의 결정적 State/Safety Engine이 최종 결정을 소유하고 Model A는 문맥 분석 또는 표현 보조로만 제한한다.

## 임시 결정

Unreal 작업은 모델 최종 선정을 기다리지 않고 `규칙 기반 Safety/State Engine + Model A 문맥 보조 + 고정 onn-c.v1 API` 구성으로 시작한다. 다음 모델 연구 세션에서는 같은 8개 사례를 모델별 최소 3회 반복하고, 안전 사례의 라벨과 문맥을 먼저 사람 검토한 뒤 분산과 warm latency를 다시 계산한다.
