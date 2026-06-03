"""Test-only HTTP fixture server for Diagnostic SBA loader QA.

This module never writes or modifies ``frontend/diagnostic-sba/preguntas.json``.
It serves the current cockpit HTML with controlled copies of the static payload.
"""

from __future__ import annotations

import argparse
import copy
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[3]
COCKPIT_PATH = ROOT / "frontend" / "diagnostic-sba" / "index.html"
PREGUNTAS_PATH = ROOT / "frontend" / "diagnostic-sba" / "preguntas.json"

SCENARIOS = (
    "valid",
    "missing",
    "forbidden",
    "server_error",
    "corrupt_json",
    "invalid_structure",
    "missing_options",
    "missing_outcome",
    "inconsistent_outcome",
    "recovery",
)


def load_payload() -> dict[str, Any]:
    with PREGUNTAS_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("preguntas.json must contain a JSON object")
    return payload


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def build_scenario_response(
    scenario: str,
    payload: dict[str, Any],
    request_count: int = 0,
) -> tuple[int, str, bytes]:
    """Return a controlled preguntas.json response without mutating ``payload``."""
    if scenario not in SCENARIOS:
        return 404, "text/plain; charset=utf-8", b"unknown scenario\n"
    if scenario == "missing":
        return 404, "text/plain; charset=utf-8", b"not found\n"
    if scenario == "forbidden":
        return 403, "text/plain; charset=utf-8", b"forbidden\n"
    if scenario == "server_error":
        return 500, "text/plain; charset=utf-8", b"server error\n"
    if scenario == "corrupt_json":
        return 200, "application/json; charset=utf-8", b'{"items": [\n'

    response_payload = copy.deepcopy(payload)
    if scenario == "invalid_structure" or (scenario == "recovery" and request_count == 0):
        response_payload["items"] = "not-a-list"
    elif scenario == "missing_options":
        response_payload["items"][0]["options"] = response_payload["items"][0]["options"][:3]
    elif scenario == "missing_outcome":
        first_item_id = response_payload["items"][0]["item_id"]
        response_payload["outcomes_by_item_id"].pop(first_item_id, None)
    elif scenario == "inconsistent_outcome":
        first_item_id = response_payload["items"][0]["item_id"]
        response_payload["outcomes_by_item_id"][first_item_id]["item_id"] = "mismatched_item_id"

    return 200, "application/json; charset=utf-8", _json_bytes(response_payload)


class LoaderQaHandler(BaseHTTPRequestHandler):
    request_counts: dict[str, int] = {}
    payload = load_payload()
    cockpit_html = COCKPIT_PATH.read_bytes()

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = urlparse(self.path).path
        parts = [part for part in path.split("/") if part]
        if len(parts) < 3 or parts[0] != "scenario" or parts[1] not in SCENARIOS:
            self._send(404, "text/plain; charset=utf-8", b"not found\n")
            return

        scenario = parts[1]
        if parts == ["scenario", scenario, "diagnostic-sba"] or parts == [
            "scenario",
            scenario,
            "diagnostic-sba",
            "index.html",
        ]:
            self._send(200, "text/html; charset=utf-8", self.cockpit_html)
            return
        if parts != ["scenario", scenario, "diagnostic-sba", "preguntas.json"]:
            self._send(404, "text/plain; charset=utf-8", b"not found\n")
            return

        request_count = self.request_counts.get(scenario, 0)
        self.request_counts[scenario] = request_count + 1
        status, content_type, body = build_scenario_response(scenario, self.payload, request_count)
        self._send(status, content_type, body)

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Serve controlled Diagnostic SBA loader QA scenarios.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18766)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), LoaderQaHandler)
    print(f"Diagnostic SBA loader QA server: http://{args.host}:{args.port}/scenario/valid/diagnostic-sba")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
