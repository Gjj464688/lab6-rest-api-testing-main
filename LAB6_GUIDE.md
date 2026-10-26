# Lab 6 - REST API Testing: Completion and Submission

**Group:** 4  
**Date:** 26 October 2026  
**Verified result:** 11 passed in 9.30 seconds (7 PyTodo tests and 4 JSONPlaceholder tests).

## Completed work

- Completed `API_FINDINGS.md` for all four required routes using actual live HTTP responses recorded before the final test run.
- Preserved and strengthened the seven Part 1 tests to check status codes, JSON headers, and relevant payloads.
- Verified the four Part 2 tests against the observed JSONPlaceholder contract.
- Added request timeouts and proper session closure.
- Removed unresolved Git conflict markers from `README.md`.
- Saved the observations and passing test results in `evidence/`.

The lab uses `requests` directly. Selenium and a browser are not needed.

## Run the tests

In PowerShell, run each command separately:

```powershell
cd 'C:\Users\Admin\Downloads\STQA\lab6-rest-api-testing-main\lab6-rest-api-testing-main'
$env:PYTODO_URL = 'https://pytodo-lab6.onrender.com'
& 'C:\Users\Admin\Downloads\STQA\Lab-5-Group-4-web-ui-automation\.venv\Scripts\python.exe' -m pytest test_api.py test_public_api.py -v
```

This uses your existing Python environment, which already contains `requests` and `pytest`. The test files remain in the Lab 6 folder.

For a separate environment on another computer:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTODO_URL = 'https://pytodo-lab6.onrender.com'
.\.venv\Scripts\python.exe -m pytest test_api.py test_public_api.py -v
```

Set `PYTODO_URL` to the Lab 6 address, rather than the Lab 5 address, in each new terminal session. The final line should show `11 passed`.

## Understand the results

Part 1 checks the PyTodo login requirement, reading tasks, valid and invalid task creation, deletion of an existing task, deletion of an absent ID, and the complete create-read-delete workflow. Tests use the IDs returned by the server. The missing-ID test confirms that its chosen ID is absent before trying to delete it.

Part 2 checks JSONPlaceholder without a login. The observed responses were:

| Method and path | Status | Response shape |
|---|---:|---|
| `GET /posts/1` | 200 | One post object |
| `GET /posts` | 200 | Array of 100 post objects |
| `POST /posts` | 201 | Submitted fields plus integer ID `101` |
| `DELETE /posts/1` | 200 | Empty object `{}` |

All four public responses had `Content-Type: application/json; charset=utf-8`. The full keys, value types, payloads, and comparison with the documentation are in `API_FINDINGS.md`.

## Evidence

| File | Contents |
|---|---|
| `evidence/public_api_observations.json` | Actual status codes, selected response headers, request bodies, timestamps, and complete JSON response bodies for all four public routes. |
| `evidence/pytest_results.txt` | The verbose output from the successful 11-test run. |
| `evidence/junit.xml` | Machine-readable test results from that same run. |

If your lecturer also wants screenshots, run the tests in your terminal and use **Windows + Shift + S**. Save the images in `evidence/`, including the final `11 passed` line. The README requires the test files and findings; it does not require an HTML report or a PDF report.

## Required submission

The lab README explicitly requires these files to be committed:

1. `test_api.py`
2. `API_FINDINGS.md`
3. `test_public_api.py`

Also include the corrected `README.md`. The updated inspection script, `.gitignore`, guide, and `evidence/` are useful supporting files.

The completed lab is connected to [your Lab 6 repository](https://github.com/Gjj464688/lab6-rest-api-testing-main). For future changes, run the following from the inner Lab 6 folder containing `test_api.py`:

```powershell
git add test_api.py test_public_api.py API_FINDINGS.md README.md Inspect_api.py .gitignore LAB6_GUIDE.md evidence/
git commit -m "Complete Lab 6 REST API tests and verified findings"
git push
```

Do not add `.venv/` or Python cache folders. The included `.gitignore` excludes them. The repository's `origin` is `https://github.com/Gjj464688/lab6-rest-api-testing-main.git`.
