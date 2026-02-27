from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


# -- Structured output schema for LLM-based extraction --
class ActionItems(BaseModel):
    """Schema enforcing Ollama to return a JSON object with an 'items' array of strings."""
    items: list[str]


DEFAULT_MODEL = "llama3.1:8b"


def _get_model_name() -> str:
    """Return the Ollama model name from OLLAMA_MODEL env var or default."""
    return os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


# -- LLM-powered extraction using Ollama with structured outputs --
def extract_action_items_llm(text: str) -> list[str]:
    """Extract action items from text using an LLM via Ollama.

    Uses structured outputs to ensure the response is a JSON array of strings.
    Returns an empty list for empty input without calling the LLM.
    """
    if not text or not text.strip():
        return []

    prompt = (
        "Extract all action items from the following text. "
        "Action items are tasks, to-dos, or things that need to be done. "
        "Return each action item as a concise, standalone string. "
        "If there are no action items, return an empty list.\n\n"
        f"Text:\n{text}"
    )

    response = chat(
        model=_get_model_name(),
        messages=[{"role": "user", "content": prompt}],
        format=ActionItems.model_json_schema(),
        options={"temperature": 0},
    )

    result = ActionItems.model_validate_json(response.message.content)
    return result.items
