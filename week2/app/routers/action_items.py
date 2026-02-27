from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemDetail,
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        try:
            note_id = db.insert_note(text)
        except Exception:
            raise HTTPException(status_code=500, detail="failed to save note")

    items = extract_action_items(text)

    try:
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to save action items")

    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    """Extract action items using an LLM via Ollama."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        try:
            note_id = db.insert_note(text)
        except Exception:
            raise HTTPException(status_code=500, detail="failed to save note")

    items = extract_action_items_llm(text)

    try:
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to save action items")

    return ExtractResponse(
        note_id=note_id,
        items=[ActionItemResponse(id=i, text=t) for i, t in zip(ids, items)],
    )


@router.get("", response_model=list[ActionItemDetail])
def list_all(note_id: Optional[int] = None) -> list[ActionItemDetail]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemDetail(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    try:
        db.mark_action_item_done(action_item_id, payload.done)
    except Exception:
        raise HTTPException(status_code=500, detail="failed to update action item")
    return MarkDoneResponse(id=action_item_id, done=payload.done)
