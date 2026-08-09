import argparse
import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from config import load_local_env
from conversation_service import ConversationService
from feedback_store import save_feedback_report
from layers.memory_layer import MemoryLayer
from ue_response import build_ue_response


DATA_DIR = Path(__file__).parent / "data" / "sessions"
REPORT_DIR = Path(__file__).parent / "data" / "reports"
SESSION_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
TURN_LOCK = threading.Lock()


def _session_memory(session_id: str) -> MemoryLayer:
    if not SESSION_PATTERN.fullmatch(session_id):
        raise ValueError("session_id must use 1-64 letters, numbers, _ or -")
    return MemoryLayer(DATA_DIR / f"{session_id}.json")


class OnionRequestHandler(BaseHTTPRequestHandler):
    server_version = "OnionConversation/1.0"

    def _write_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._write_json(200, {"status": "ok", "schema_version": "onn-c.v1"})
            return
        self._write_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        if self.path not in {"/v1/conversations/respond", "/v1/feedback/reports"}:
            self._write_json(404, {"error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 64_000:
                raise ValueError("request body must be between 1 and 64000 bytes")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("request body must be a JSON object")
            if self.path == "/v1/feedback/reports":
                report = save_feedback_report(payload, REPORT_DIR)
                self._write_json(
                    201,
                    {
                        "report_id": report["report_id"],
                        "status": report["status"],
                        "content_included": report["content_included"],
                    },
                )
                return

            message = payload.get("message")
            session_id = payload.get("session_id", "ue-local")
            use_nvidia = payload.get("use_nvidia", True)
            if not isinstance(message, str) or not message.strip():
                raise ValueError("message must be a non-empty string")
            if not isinstance(session_id, str):
                raise ValueError("session_id must be a string")
            if not isinstance(use_nvidia, bool):
                raise ValueError("use_nvidia must be a boolean")

            with TURN_LOCK:
                service = ConversationService(
                    _session_memory(session_id),
                    use_nvidia=use_nvidia,
                )
                turn = service.respond(message.strip())
            self._write_json(200, build_ue_response(turn.result, turn.expression))
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            self._write_json(400, {"error": "invalid_request", "detail": str(error)})
        except Exception:
            self._write_json(500, {"error": "internal_error"})

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ONN-C JSON API for Unreal Engine.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    return parser.parse_args()


def main() -> None:
    load_local_env()
    args = _parse_args()
    server = ThreadingHTTPServer((args.host, args.port), OnionRequestHandler)
    print(f"ONN-C API listening on http://{args.host}:{args.port}")
    print("POST /v1/conversations/respond, POST /v1/feedback/reports, or GET /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ONN-C API.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
