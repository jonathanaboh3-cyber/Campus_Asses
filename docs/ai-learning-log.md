# AI Learning Log: Engineer A (Registration and Data Safety)

## How AI was used in my part

**My work**

- The starting point was my own `registration.py`, which I had already run: `create_request`, `get_request`, `save_requests`, `load_requests`, input validation and the ID counter. Running it printed a request with ID A004, which showed that IDs depend on what is already saved in `requests.json`.
- I set up the project structure (`campus_access/`, `main.py`, `tests/`, `docs/`) and got everything running on my machine: I switched from `python` to `python3`, found that I had to run commands from the top `Campus_Access` folder, and fixed the import line in `tests/test_registration.py`.
- I ran the unit tests myself: `python3 -m unittest discover -s tests -v` ran 8 tests and all 8 passed.

**What AI (Claude) suggested or drafted**

- Found that duplicate IDs in a JSON file were not being rejected, and suggested the `object_pairs_hook` fix (learning cycle 1).
- Suggested saving through a temporary file (learning cycle 2).
- Suggested a separate `validate_request_id` function that checks ASCII digits (learning cycle 3), and moving the allowed values into constants at the top of the file.
- Drafted the first version of the 8 unit tests in `tests/test_registration.py`.

**Advice I verified and adjusted**

- AI first gave me `python3 -m unittest discover -s tests -t . -v`. In my folder it failed with "Start directory is not importable" because `tests/` had no `__init__.py`. I used the command from the assignment instead, `python3 -m unittest discover -s tests -v`, and it worked.
- AI told me to change the import in the test file to `from campus_access import registration`. The first attempt did not change the right line, so the same error came back. After the change was applied correctly, all 8 tests ran and passed.

---

## Learning cycle 1: Do duplicate IDs in a JSON file get caught?

**Question:** My first `load_requests` had a `seen_ids` check for duplicate IDs. Can that check ever trigger when I load a file with `json.load`?

**Explanation:** `json.load` turns a JSON object into a Python dictionary. A dictionary cannot hold two equal keys, so Python silently keeps the last one and drops the first. The `seen_ids` loop therefore never sees a duplicate, and a file with two `"A001"` entries would be accepted without any error. The fix is to pass `object_pairs_hook` to `json.load`. It receives the raw key/value pairs before the dictionary is built, so the code can raise `ValueError` when a key appears twice.

**How to see it:** `python3 -c "import json; print(json.loads('{\"A001\": 1, \"A001\": 2}'))"` prints `{'A001': 2}`. The first value is gone and no error is raised.

**Verification:** The test `test_duplicate_ids_in_file_rejected` writes a file with `"A001"` twice and expects `ValueError` from `load_requests`. It passed in my run (8 tests, OK).

**Decision:** I kept `_reject_duplicate_keys` with `object_pairs_hook` and removed the old `seen_ids` check, because that check could never trigger.

---

## Learning cycle 2: Can a failed save destroy a valid file?

**Question:** The assignment asks how to test that a failed save does not overwrite a valid file. If `open(path, "w")` empties the file before `json.dump` fails, what is left on disk?

**Explanation:** Opening a file in `"w"` mode erases its contents immediately. If `json.dump` then fails halfway, the old good data is already gone. The safer way is to write the new data to a temporary file and call `os.replace(temp_path, path)` only after the write has fully succeeded. If anything fails first, the real file is never touched, and the temp file is deleted.

**Verification:** The test `test_failed_save_does_not_overwrite_valid_file` saves one valid request, adds a value JSON cannot store (a Python `set`), expects the save to raise `TypeError`, and checks that the file content is exactly the same as before. It passed in my run (8 tests, OK).

**Decision:** I kept the temp-file approach in `save_requests`.

---

## Learning cycle 3: Why `isdigit()` is not enough for ID checks

**Question:** The assignment says to accept only ASCII digits 0-9 in request IDs. Does `isdigit()` alone do that?

**Explanation:** No. `isdigit()` is also true for digits from other scripts, such as the Arabic-Indic digits. Adding `isascii()` rejects them, so `validate_request_id` checks both.

**How to see it:** `python3 -c "s = 'A١٢٣'; print(s[1:].isdigit(), s[1:].isascii())"` prints `True False`.

**Verification:** The test `test_malformed_request_id_rejected` includes an ID built with Arabic-Indic digits, along with `B001`, `A1`, `A00` and the number `1`. All were rejected, and the test passed in my run.

**Decision:** I kept both checks (`isascii()` and `isdigit()`) in `validate_request_id`.