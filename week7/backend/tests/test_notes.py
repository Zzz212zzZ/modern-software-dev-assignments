def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_put_note_updates_title_and_content(client):
    # Create a note to operate on
    r = client.post("/notes/", json={"title": "Original Title", "content": "Original content"})
    assert r.status_code == 201, r.text
    note = r.json()
    note_id = note["id"]
    original_updated_at = note["updated_at"]

    # PUT requires both title and content (full replacement)
    r = client.put(f"/notes/{note_id}", json={"title": "New Title", "content": "New content"})
    assert r.status_code == 200, r.text
    updated = r.json()

    assert updated["id"] == note_id
    assert updated["title"] == "New Title"
    assert updated["content"] == "New content"
    assert "created_at" in updated
    assert "updated_at" in updated
    # updated_at should have advanced (or at minimum be present)
    assert updated["updated_at"] >= original_updated_at


def test_put_note_returns_404_for_missing_note(client):
    # Use an ID that was never created
    r = client.put("/notes/99999", json={"title": "Ghost", "content": "Nobody home"})
    assert r.status_code == 404, r.text


def test_put_note_requires_both_fields(client):
    # Create a note so we have a valid ID
    r = client.post("/notes/", json={"title": "To Replace", "content": "Some content"})
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # PUT with only title and no content must be rejected
    r = client.put(f"/notes/{note_id}", json={"title": "Only Title"})
    assert r.status_code == 422, r.text
