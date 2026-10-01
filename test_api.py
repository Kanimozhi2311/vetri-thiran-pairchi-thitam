from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_json_generation_in_demo_mode():
    payload = {
        "story_prompt": "A brave fox explores an enchanted forest.",
        "character_name": "Lumi", "setting": "forest",
        "tone": "dramatic", "art_style": "anime",
    }
    response = client.post("/generate-comic/json", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["panels"]) == 5
    assert data["pdf_url"].startswith("/download/")
