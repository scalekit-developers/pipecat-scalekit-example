"""Unit tests at the Scalekit seams. Scalekit is mocked."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest


def test_get_scalekit_fails_when_env_url_missing(monkeypatch):
    monkeypatch.delenv("SCALEKIT_ENV_URL", raising=False)
    monkeypatch.delenv("SCALEKIT_ENVIRONMENT_URL", raising=False)
    monkeypatch.setenv("SCALEKIT_CLIENT_ID", "skc_test")
    monkeypatch.setenv("SCALEKIT_CLIENT_SECRET", "skcs_test")

    import scalekit_calendar as sc

    sc.reset_scalekit()
    with pytest.raises(RuntimeError, match="SCALEKIT"):
        sc.get_scalekit()


def test_get_scalekit_uses_environment_url_alias(monkeypatch):
    monkeypatch.delenv("SCALEKIT_ENV_URL", raising=False)
    monkeypatch.setenv("SCALEKIT_ENVIRONMENT_URL", "https://env.example")
    monkeypatch.setenv("SCALEKIT_CLIENT_ID", "skc_test")
    monkeypatch.setenv("SCALEKIT_CLIENT_SECRET", "skcs_test")

    import scalekit_calendar as sc

    sc.reset_scalekit()
    fake_cls = MagicMock(return_value=MagicMock())
    monkeypatch.setattr(sc, "ScalekitClient", fake_cls)
    client = sc.get_scalekit()
    fake_cls.assert_called_once_with("https://env.example", "skc_test", "skcs_test")
    assert client is fake_cls.return_value


def test_list_calendar_events_calls_execute_tool_as_identifier():
    import scalekit_calendar as sc

    client = MagicMock()
    client.actions.execute_tool.return_value = MagicMock(data={"events": []})
    result = sc.list_calendar_events(
        client=client,
        identifier="user@example.com",
        connection_name="googlecalendar",
        calendar_id="primary",
        time_min="2026-09-20T00:00:00Z",
        time_max="2026-09-27T00:00:00Z",
    )
    kwargs = client.actions.execute_tool.call_args.kwargs
    assert kwargs["tool_name"] == "googlecalendar_list_events"
    assert kwargs["identifier"] == "user@example.com"
    assert kwargs["connection_name"] == "googlecalendar"
    assert kwargs["tool_input"]["calendar_id"] == "primary"
    assert result == {"events": []}


def test_list_calendar_events_strips_token_fields():
    import scalekit_calendar as sc

    client = MagicMock()
    client.actions.execute_tool.return_value = MagicMock(
        data={
            "events": [{"summary": "Standup"}],
            "access_token": "ya29.secret",
            "refresh_token": "1//secret",
        }
    )
    result = sc.list_calendar_events(
        client=client,
        identifier="user@example.com",
        connection_name="googlecalendar",
    )
    assert result["events"] == [{"summary": "Standup"}]
    assert "access_token" not in result
    assert "refresh_token" not in result
    dumped = json.dumps(result)
    assert "ya29.secret" not in dumped
    assert "1//secret" not in dumped


def test_list_calendar_events_returns_error_dict_not_raise():
    import scalekit_calendar as sc

    client = MagicMock()
    client.actions.execute_tool.side_effect = RuntimeError("connection not found")
    result = sc.list_calendar_events(
        client=client,
        identifier="user@example.com",
        connection_name="googlecalendar",
    )
    assert result == {"error": "connection not found"}
    assert "token" not in result


def test_list_calendar_events_errors_when_connected_account_id_missing(monkeypatch):
    monkeypatch.delenv("CONNECTED_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("TEST_IDENTIFIER", raising=False)

    import scalekit_calendar as sc

    result = sc.list_calendar_events(client=MagicMock())
    assert "error" in result
    assert "CONNECTED_ACCOUNT_ID" in result["error"]
    assert "TEST_IDENTIFIER" not in result["error"]


def test_list_calendar_events_uses_connected_account_id_from_env(monkeypatch):
    monkeypatch.setenv("CONNECTED_ACCOUNT_ID", "dev@example.com")

    import scalekit_calendar as sc

    client = MagicMock()
    client.actions.execute_tool.return_value = MagicMock(data={"events": []})
    result = sc.list_calendar_events(client=client, connection_name="googlecalendar")
    assert client.actions.execute_tool.call_args.kwargs["identifier"] == "dev@example.com"
    assert result == {"events": []}


def test_list_calendar_events_does_not_fall_back_to_test_identifier(monkeypatch):
    monkeypatch.delenv("CONNECTED_ACCOUNT_ID", raising=False)
    monkeypatch.setenv("TEST_IDENTIFIER", "old@example.com")

    import scalekit_calendar as sc

    result = sc.list_calendar_events(client=MagicMock())
    assert result == {"error": "CONNECTED_ACCOUNT_ID is not set"}
