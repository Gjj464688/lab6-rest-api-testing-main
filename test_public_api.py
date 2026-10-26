"""Part 2: tests against JSONPlaceholder, a public API.

Run with:
    pytest test_public_api.py -v
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
REQUEST_TIMEOUT = 30


def test_get_single_post():
    """GET /posts/1."""
    response = requests.get(f"{BASE_URL}/posts/1", timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == (
        "application/json; charset=utf-8"
    )

    body = response.json()

    assert isinstance(body, dict)
    assert body["id"] == 1
    assert isinstance(body["userId"], int)
    assert isinstance(body["id"], int)
    assert isinstance(body["title"], str)
    assert isinstance(body["body"], str)


def test_get_all_posts():
    """GET /posts."""
    response = requests.get(f"{BASE_URL}/posts", timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == (
        "application/json; charset=utf-8"
    )

    body = response.json()

    assert isinstance(body, list)
    assert len(body) == 100

    for post in body:
        assert isinstance(post, dict)
        assert isinstance(post["userId"], int)
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)


def test_create_post():
    """POST /posts."""
    payload = {
        "title": "",
        "body": "",
        "userId": 1,
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"] == (
        "application/json; charset=utf-8"
    )

    body = response.json()

    assert isinstance(body, dict)
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body
    assert isinstance(body["id"], int)


def test_delete_post():
    """DELETE /posts/1."""
    response = requests.delete(f"{BASE_URL}/posts/1", timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == (
        "application/json; charset=utf-8"
    )
    assert response.json() == {}
