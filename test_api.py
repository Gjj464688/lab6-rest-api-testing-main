"""Lab 6: test the PyTodo JSON API directly, with no browser.

Demo login:
    username: demo
    password: demo1234

The API uses the same login as a normal browser session. requests.Session()
keeps the login cookie between calls, the same way a browser keeps it
between page loads. Log in once per test with the logged_in_session
fixture below, already written for you.

Run with:
    pytest test_api.py -v

Seven tests cover authentication, JSON responses, input validation,
deletion, and a full create-read-delete workflow.
"""
import os

import pytest
import requests

BASE_URL = os.environ.get("PYTODO_URL", "http://127.0.0.1:5000").rstrip("/")
REQUEST_TIMEOUT = 30


@pytest.fixture
def logged_in_session():
    """Returns a requests.Session already logged in as the demo user."""
    s = requests.Session()
    try:
        response = s.post(
            f"{BASE_URL}/login",
            data={"username": "demo", "password": "demo1234"},
            timeout=REQUEST_TIMEOUT,
        )
        assert response.status_code == 200
        yield s
    finally:
        s.close()


# ============================================================
# GET /api/tasks - authentication and the task list
# ============================================================

def test_get_tasks_requires_login():
    # A plain requests call, no session, no login.
    response = requests.get(f"{BASE_URL}/api/tasks", timeout=REQUEST_TIMEOUT)
    assert response.status_code == 401
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"error": "login required"}


def test_get_tasks_returns_json_list(logged_in_session):
    response = logged_in_session.get(f"{BASE_URL}/api/tasks", timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert isinstance(response.json(), list)


# ============================================================
# POST /api/tasks - valid and invalid input
# ============================================================

def test_create_task_with_valid_data(logged_in_session):
    payload = {"title": "Write report", "priority": 3, "due_date": "2026-12-01"}
    response = logged_in_session.post(
        f"{BASE_URL}/api/tasks", json=payload, timeout=REQUEST_TIMEOUT
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"

    body = response.json()
    assert body["title"] == "Write report"
    assert body["priority"] == 3
    assert body["due_date"] == "2026-12-01"
    assert body["completed"] is False
    assert "id" in body
    assert isinstance(body["id"], int)


def test_create_task_with_invalid_data(logged_in_session):
    payload = {
        "title": "ab",
        "priority": 9,
        "due_date": "2026-12-01",
    }

    response = logged_in_session.post(
        f"{BASE_URL}/api/tasks",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    assert response.status_code == 400
    assert response.headers["Content-Type"] == "application/json"

    body = response.json()
    assert "errors" in body
    assert isinstance(body["errors"], list)
    assert len(body["errors"]) > 0


# ============================================================
# DELETE /api/tasks/<id> - existing and missing tasks
# ============================================================

def test_delete_existing_task(logged_in_session):
    payload = {
        "title": "Task to delete",
        "priority": 3,
        "due_date": "2026-12-01",
    }

    create_response = logged_in_session.post(
        f"{BASE_URL}/api/tasks",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    assert create_response.status_code == 201
    assert create_response.headers["Content-Type"] == "application/json"
    task_id = create_response.json()["id"]

    response = logged_in_session.delete(
        f"{BASE_URL}/api/tasks/{task_id}", timeout=REQUEST_TIMEOUT
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {
        "status": "deleted",
        "id": task_id,
    }


def test_delete_missing_task_returns_404(logged_in_session):
    # Confirm this ID is absent before issuing the DELETE request.
    existing = logged_in_session.get(
        f"{BASE_URL}/api/tasks", timeout=REQUEST_TIMEOUT
    )
    assert existing.status_code == 200
    assert existing.headers["Content-Type"] == "application/json"
    assert isinstance(existing.json(), list)
    assert all(task["id"] != 999999 for task in existing.json())

    response = logged_in_session.delete(
        f"{BASE_URL}/api/tasks/999999", timeout=REQUEST_TIMEOUT
    )

    assert response.status_code == 404
    assert response.headers["Content-Type"] == "application/json"
    body = response.json()
    assert isinstance(body, dict)
    assert isinstance(body.get("error"), str)
    assert body["error"]


# ============================================================
# Full flow - create, read it back, delete, confirm it is gone
# ============================================================

def test_create_read_delete_flow(logged_in_session):
    payload = {
        "title": "Flow test task",
        "priority": 2,
        "due_date": "2026-12-15",
    }

    create_response = logged_in_session.post(
        f"{BASE_URL}/api/tasks",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    assert create_response.status_code == 201
    assert create_response.headers["Content-Type"] == "application/json"
    task_id = create_response.json()["id"]

    # Confirm that the task appears in the task list.
    list_response = logged_in_session.get(
        f"{BASE_URL}/api/tasks", timeout=REQUEST_TIMEOUT
    )

    assert list_response.status_code == 200
    assert list_response.headers["Content-Type"] == "application/json"
    tasks = list_response.json()
    assert isinstance(tasks, list)
    assert any(task["id"] == task_id for task in tasks)

    # Delete the task.
    delete_response = logged_in_session.delete(
        f"{BASE_URL}/api/tasks/{task_id}", timeout=REQUEST_TIMEOUT
    )

    assert delete_response.status_code == 200
    assert delete_response.headers["Content-Type"] == "application/json"
    assert delete_response.json() == {"status": "deleted", "id": task_id}

    # Confirm that the task no longer appears.
    final_response = logged_in_session.get(
        f"{BASE_URL}/api/tasks", timeout=REQUEST_TIMEOUT
    )

    assert final_response.status_code == 200
    assert final_response.headers["Content-Type"] == "application/json"
    remaining_tasks = final_response.json()
    assert isinstance(remaining_tasks, list)
    assert all(task["id"] != task_id for task in remaining_tasks)
