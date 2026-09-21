"""Scalekit AgentKit helpers. The LLM never sees an OAuth token."""

from __future__ import annotations

import json
import os
from typing import Any

from scalekit import ScalekitClient

_scalekit: ScalekitClient | None = None


def _env(*names: str, environ: dict[str, str] | None = None) -> str:
    source = environ if environ is not None else os.environ
    for name in names:
        value = (source.get(name) or "").strip()
        if value:
            return value
    return ""


def reset_scalekit() -> None:
    global _scalekit
    _scalekit = None


def get_scalekit() -> ScalekitClient:
    global _scalekit
    if _scalekit is None:
        env_url = _env("SCALEKIT_ENV_URL", "SCALEKIT_ENVIRONMENT_URL")
        client_id = _env("SCALEKIT_CLIENT_ID")
        client_secret = _env("SCALEKIT_CLIENT_SECRET")
        if not env_url or not client_id or not client_secret:
            raise RuntimeError(
                "Missing SCALEKIT_ENV_URL, SCALEKIT_CLIENT_ID, or SCALEKIT_CLIENT_SECRET."
            )
        _scalekit = ScalekitClient(env_url, client_id, client_secret)
    return _scalekit


_TOKEN_KEYS = frozenset(
    {
        "access_token",
        "refresh_token",
        "id_token",
        "token",
        "oauth_token",
        "client_secret",
        "api_key",
        "authorization",
        "bearer",
    }
)


def _without_tokens(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_tokens(item)
            for key, item in value.items()
            if key.lower() not in _TOKEN_KEYS
        }
    if isinstance(value, list):
        return [_without_tokens(item) for item in value]
    return value


def _speakable(value: Any) -> dict:
    if value is None:
        return {"ok": True}
    if hasattr(value, "to_dict"):
        return _speakable(value.to_dict())
    if isinstance(value, dict):
        return _without_tokens(value)
    if hasattr(value, "items"):
        try:
            return _without_tokens(dict(value))
        except Exception:
            pass
    try:
        parsed = json.loads(json.dumps(value, default=str))
        cleaned = _without_tokens(parsed)
        return cleaned if isinstance(cleaned, dict) else {"data": cleaned}
    except Exception:
        return {"data": str(value)}


def list_calendar_events(
    *,
    client: Any | None = None,
    identifier: str | None = None,
    connection_name: str | None = None,
    calendar_id: str = "primary",
    time_min: str = "",
    time_max: str = "",
    max_results: int = 10,
) -> dict:
    identifier = identifier if identifier is not None else _env("CONNECTED_ACCOUNT_ID")
    connection_name = connection_name or _env("SCALEKIT_CONNECTION_NAME") or "googlecalendar"
    if not identifier:
        return {"error": "CONNECTED_ACCOUNT_ID is not set"}

    tool_input: dict[str, Any] = {
        "calendar_id": calendar_id or "primary",
        "max_results": max_results or 10,
        "single_events": True,
        "order_by": "startTime",
    }
    if time_min:
        tool_input["time_min"] = time_min
    if time_max:
        tool_input["time_max"] = time_max

    sdk = client if client is not None else get_scalekit()
    try:
        response = sdk.actions.execute_tool(
            tool_input=tool_input,
            tool_name="googlecalendar_list_events",
            identifier=identifier,
            connection_name=connection_name,
        )
        payload = getattr(response, "data", response)
        return _speakable(payload)
    except Exception as exc:
        return {"error": str(exc)}
