"""Pydantic request/response models for well-defined API contracts."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


# -- Requests --

class NoteCreate(BaseModel):
    content: str


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class MarkDoneRequest(BaseModel):
    done: bool = True


# -- Responses --

class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ActionItemResponse(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: list[ActionItemResponse]


class ActionItemDetail(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


class MarkDoneResponse(BaseModel):
    id: int
    done: bool
