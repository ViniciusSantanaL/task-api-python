import pytest
import requests

BASE_URL = "http://0.0.0.0:3000/"

task_slugs = []


def test_create_task():
    new_task_request = {
        "title": "New Task",
        "description": "test"
    }
    response = requests.post(f"{BASE_URL}/task", json=new_task_request)
    response_json = response.json()
    assert response.status_code is 201
    assert response_json["slug"] is not None
    assert response_json["title"] == new_task_request["title"]
    assert response_json["description"] == new_task_request["description"]
    assert response_json["completed"] is False
    task_slugs.append(response_json["slug"])


def test_get_all_tasks():
    response = requests.get(f"{BASE_URL}/task")
    response_json = response.json()

    assert response.status_code is 200
    assert response_json["total"] is not None
    assert response_json["tasks"] is not None


def test_get_task_by_slug():
    if task_slugs:
        slug = task_slugs[0]
        response = requests.get(f"{BASE_URL}/task/{slug}")
        response_json = response.json()

        assert response.status_code is 200
        assert response_json["slug"] is not None
        assert response_json["title"] is not None
        assert response_json["description"] is not None
        assert response_json["completed"] is not None


def test_update_task():
    if task_slugs:
        slug = task_slugs[0]
        task_to_update_payload = {
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        }

        response_task_updated = requests.put(f"{BASE_URL}/task/{slug}", json=task_to_update_payload)

        task_updated = response_task_updated.json()
        assert task_updated["slug"] == slug
        assert task_updated["title"] == 'Updated Task'
        assert task_updated["description"] == "Updated Description"
        assert task_updated["completed"] is True

