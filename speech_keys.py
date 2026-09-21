"""Required Deepgram and Cartesia keys. This sample has no local-speech fallback."""

from __future__ import annotations

import os
from typing import Mapping

DEEPGRAM_SIGNUP_URL = "https://console.deepgram.com/signup"
CARTESIA_SIGNUP_URL = "https://play.cartesia.ai"


def require_speech_keys(environ: Mapping[str, str] | None = None) -> tuple[str, str]:
    source = environ if environ is not None else os.environ
    deepgram = (source.get("DEEPGRAM_API_KEY") or "").strip()
    cartesia = (source.get("CARTESIA_API_KEY") or "").strip()
    if not deepgram or not cartesia:
        raise RuntimeError(
            "Missing DEEPGRAM_API_KEY or CARTESIA_API_KEY. "
            f"Get a Deepgram key at {DEEPGRAM_SIGNUP_URL}. "
            f"Get a Cartesia key at {CARTESIA_SIGNUP_URL}."
        )
    return deepgram, cartesia
