"""Prove Scalekit googlecalendar_list_events without the voice stack.

The LLM never sees a token. This script calls execute_tool as CONNECTED_ACCOUNT_ID.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from scalekit import ScalekitClient

load_dotenv(override=True)


def _env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def main() -> int:
    env_url = _env("SCALEKIT_ENV_URL", "SCALEKIT_ENVIRONMENT_URL")
    client_id = _env("SCALEKIT_CLIENT_ID")
    client_secret = _env("SCALEKIT_CLIENT_SECRET")
    identifier = _env("CONNECTED_ACCOUNT_ID")
    connection_name = _env("SCALEKIT_CONNECTION_NAME") or "googlecalendar"

    missing = [
        name
        for name, value in [
            ("SCALEKIT_ENV_URL", env_url),
            ("SCALEKIT_CLIENT_ID", client_id),
            ("SCALEKIT_CLIENT_SECRET", client_secret),
            ("CONNECTED_ACCOUNT_ID", identifier),
        ]
        if not value
    ]
    if missing:
        print("FAIL missing env:", ", ".join(missing), file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)
    tool_input = {
        "calendar_id": "primary",
        "max_results": 5,
        "single_events": True,
        "order_by": "startTime",
        "time_min": start.isoformat().replace("+00:00", "Z"),
        "time_max": end.isoformat().replace("+00:00", "Z"),
    }

    client = ScalekitClient(env_url, client_id, client_secret)
    response = client.actions.execute_tool(
        tool_input=tool_input,
        tool_name="googlecalendar_list_events",
        identifier=identifier,
        connection_name=connection_name,
    )
    data = response.data if hasattr(response, "data") else response
    payload = data if isinstance(data, dict) else {"data": data}

    events = []
    if isinstance(payload, dict):
        events = payload.get("events") or payload.get("items") or []
        if not events and isinstance(payload.get("data"), dict):
            inner = payload["data"]
            events = inner.get("events") or inner.get("items") or []

    print("PASS execute_tool googlecalendar_list_events")
    print("identifier_set", bool(identifier))
    print("connection_name", connection_name)
    print("execution_id", getattr(response, "execution_id", None))
    print("event_count", len(events) if isinstance(events, list) else 0)
    if isinstance(events, list):
        for event in events[:3]:
            if not isinstance(event, dict):
                continue
            summary = event.get("summary") or event.get("title") or "(no title)"
            start_at = event.get("start") or event.get("start_time") or ""
            print("event", summary, start_at)
    else:
        print(json.dumps(payload, default=str)[:500])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("FAIL", exc, file=sys.stderr)
        raise SystemExit(1)
