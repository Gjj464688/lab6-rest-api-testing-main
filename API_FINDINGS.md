# API Findings: JSONPlaceholder

**Testers:** Ahmad Adam Ali, Gan Jeng Jie, Wan Qistina
**Date:** 26 October 2026  
**Application:** https://jsonplaceholder.typicode.com  
**Method:** Actual HTTP requests sent with Python `requests`, before finalizing the tests.  
**Observation window:** 11:10:32-11:10:34, Asia/Singapore (UTC+08:00).

The status codes, headers, and bodies below were read from the live responses. The complete observations are saved in `evidence/public_api_observations.json`.

## GET /posts/1

| Field | Observed value |
|---|---|
| Method and path | `GET /posts/1` |
| Status code | `200` |
| Content-Type | `application/json; charset=utf-8` |
| Body shape | JSON object |

| Key | JSON type | Observed example |
|---|---|---|
| `userId` | Integer | `1` |
| `id` | Integer | `1` |
| `title` | String | `sunt aut facere repellat provident occaecati excepturi optio reprehenderit` |
| `body` | String | Contains text and newline characters; full value below. |

Actual response:

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

## GET /posts

| Field | Observed value |
|---|---|
| Method and path | `GET /posts` |
| Status code | `200` |
| Content-Type | `application/json; charset=utf-8` |
| Body shape | JSON array of 100 objects |

Each array element has these keys and types:

| Key | JSON type | First object's value |
|---|---|---|
| `userId` | Integer | `1` |
| `id` | Integer | `1` |
| `title` | String | Same title as the `GET /posts/1` response above. |
| `body` | String | Same body as the `GET /posts/1` response above. |

The full 100-object response is preserved in the observations file rather than abbreviated as if it were the complete response.

## POST /posts

| Field | Observed value |
|---|---|
| Method and path | `POST /posts` |
| Status code | `201` |
| Content-Type | `application/json; charset=utf-8` |
| Body shape | JSON object |

Request body sent:

```json
{
  "title": "",
  "body": "",
  "userId": 1
}
```

Actual response:

```json
{
  "title": "",
  "body": "",
  "userId": 1,
  "id": 101
}
```

| Key | JSON type | Observed value |
|---|---|---|
| `title` | String | Empty string |
| `body` | String | Empty string |
| `userId` | Integer | `1` |
| `id` | Integer | `101` |

The server accepted empty title and body strings, echoed the submitted fields, and supplied an integer ID. It did not return a validation-error response. These are observations from this payload; they do not establish behavior for every possible invalid payload.

## DELETE /posts/1

| Field | Observed value |
|---|---|
| Method and path | `DELETE /posts/1` |
| Status code | `200` |
| Content-Type | `application/json; charset=utf-8` |
| Body shape | Empty JSON object |

Actual response:

```json
{}
```

There are no response-body keys or value types to enumerate. The response contains an empty object, rather than an empty response body, so `response.json()` returns `{}`.

## Comparison with the API documentation

The observed GET payloads, POST response structure, and empty DELETE object agree with the examples in the [official guide](https://jsonplaceholder.typicode.com/guide). No disagreement was observed for the four recorded requests. The guide's POST example uses non-empty strings; our additional observation is that the empty strings in the recorded request were accepted too.

The guide states that writes are simulated and do not persist on the server. Consequently, this public API's tests check the returned contract rather than applying PyTodo's persistent create-read-delete workflow to it.
