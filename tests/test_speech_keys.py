"""Unit tests for required Deepgram and Cartesia keys."""

from __future__ import annotations

import pytest

from speech_keys import require_speech_keys


def test_require_speech_keys_ok_when_both_present():
    deepgram, cartesia = require_speech_keys(
        environ={"DEEPGRAM_API_KEY": "dg-key", "CARTESIA_API_KEY": "ca-key"}
    )
    assert deepgram == "dg-key"
    assert cartesia == "ca-key"


def test_require_speech_keys_errors_when_missing():
    with pytest.raises(RuntimeError, match="DEEPGRAM_API_KEY") as exc:
        require_speech_keys(environ={})
    message = str(exc.value)
    assert "CARTESIA_API_KEY" in message
    assert "Deepgram" in message
    assert "Cartesia" in message
    assert "console.deepgram.com" in message
    assert "cartesia.ai" in message
