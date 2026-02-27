import json
from unittest.mock import MagicMock, patch

from ..app.services.extract import extract_action_items, extract_action_items_llm


# ---------- Existing heuristic tests ----------

def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ---------- Helper for mocking Ollama chat responses ----------

def _mock_chat_response(items: list[str]) -> MagicMock:
    """Build a mock Ollama chat response containing the given items."""
    resp = MagicMock()
    resp.message.content = json.dumps({"items": items})
    return resp


# ---------- LLM extraction unit tests ----------

@patch("week2.app.services.extract.chat")
def test_llm_empty_input(mock_chat):
    """Empty and whitespace-only input should return [] without calling the LLM."""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    mock_chat.assert_not_called()


@patch("week2.app.services.extract.chat")
def test_llm_bullet_list(mock_chat):
    """Bullet-list input should be sent to the LLM and parsed correctly."""
    mock_chat.return_value = _mock_chat_response(
        ["Set up database", "Implement API endpoint", "Write tests"]
    )

    text = "- Set up database\n- Implement API endpoint\n- Write tests"
    result = extract_action_items_llm(text)

    assert result == ["Set up database", "Implement API endpoint", "Write tests"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_llm_keyword_prefixed(mock_chat):
    """Keyword-prefixed lines (todo:, action:, next:) should be extracted."""
    mock_chat.return_value = _mock_chat_response(
        ["Buy milk", "Fix login bug", "Deploy to production"]
    )

    text = "todo: Buy milk\naction: Fix login bug\nnext: Deploy to production"
    result = extract_action_items_llm(text)

    assert result == ["Buy milk", "Fix login bug", "Deploy to production"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_llm_narrative_text(mock_chat):
    """Free-form prose with embedded tasks should have action items extracted."""
    mock_chat.return_value = _mock_chat_response(
        ["Schedule team meeting", "Update project README"]
    )

    text = (
        "Had a great day at the office. We need to schedule team meeting "
        "before Friday. Also, someone should update project README with "
        "the new API docs."
    )
    result = extract_action_items_llm(text)

    assert result == ["Schedule team meeting", "Update project README"]
    mock_chat.assert_called_once()


@patch("week2.app.services.extract.chat")
def test_llm_no_action_items(mock_chat):
    """Text with no actionable content should return an empty list."""
    mock_chat.return_value = _mock_chat_response([])

    result = extract_action_items_llm("The weather is nice today.")

    assert result == []
    mock_chat.assert_called_once()
