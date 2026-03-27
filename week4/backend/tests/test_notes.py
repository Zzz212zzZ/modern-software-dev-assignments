def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_delete_note(client):
    # Create a note
    payload = {"title": "To Delete", "content": "This will be deleted"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # Delete the note
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204, r.text
    assert r.content == b""  # 204 should have no content

    # Verify the note is gone
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404, r.text


def test_delete_nonexistent_note(client):
    # Try to delete a note that doesn't exist
    r = client.delete("/notes/99999")
    assert r.status_code == 404, r.text
