import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

routes = [
    ("GET", "/posts/1", None),
    ("GET", "/posts", None),
    ("POST", "/posts", {
        "title": "",
        "body": "",
        "userId": 1,
    }),
    ("DELETE", "/posts/1", None),
]

for method, path, payload in routes:
    response = requests.request(
        method,
        f"{BASE_URL}{path}",
        json=payload,
        timeout=30,
    )

    print(f"\n{'=' * 50}")
    print(f"{method} {path}")
    print("Status code:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("Response body:", response.text[:500])

    if response.text:
        try:
            data = response.json()

            if isinstance(data, dict):
                print("Body type: object")
                print("Keys and types:", {
                    key: type(value).__name__
                    for key, value in data.items()
                })

            elif isinstance(data, list):
                print("Body type: array")
                print("Number of items:", len(data))

                if data:
                    print("First item's keys and types:", {
                        key: type(value).__name__
                        for key, value in data[0].items()
                    })

        except ValueError:
            print("Response is not JSON")
    else:
        print("Response body is empty")
