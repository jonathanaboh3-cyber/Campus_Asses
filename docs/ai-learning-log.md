# AI Learning Log: Engineer A (Registration and Data Safety)

> Fill in every [BRACKET] yourself after you run the experiment. Only write what you actually did and saw. Do not claim you ran something you did not.

## How AI was used in my part

- AI (Claude) supplied a first version of `campus_access/registration.py` and of `tests/test_registration.py`, because I had limited time.
- AI helped me fix a bug: duplicate IDs in a JSON file were not being rejected.
- What I changed or wrote myself: [FILL IN, e.g. "I wrote tests X and Y myself", "I renamed ..."]
- Parts I can now explain without AI: [FILL IN]
- Parts I still need to study: [FILL IN]

---

## Learning cycle 1: Do duplicate IDs in a JSON file get caught?

**Question I asked:** My first `load_requests` had a `seen_ids` check for duplicate IDs. Can that check ever trigger when I load a file with `json.load`?

**My prediction (write this BEFORE running the experiment):** [FILL IN, e.g. "json.load will raise an error on duplicate keys" or "it will keep one of them"]

**AI explanation (in my own words):** `json.load` turns a JSON object into a Python dictionary. A dictionary cannot hold two equal keys, so Python silently keeps the last one and drops the first. That means the `seen_ids` loop never saw a duplicate, and a file with two `"A001"` entries was accepted without any error. The fix is to pass `object_pairs_hook` to `json.load`, which receives the raw key/value pairs before the dictionary is built, so I can raise `ValueError` when a key appears twice.

**My own experiment:** I ran this in the terminal:

```
python3 -c "import json; print(json.loads('{\"A001\": 1, \"A001\": 2}'))"
```

Result I saw: [FILL IN what printed]

**Verification:** I ran `python3 -m unittest discover -s tests -v`. The test `test_duplicate_ids_in_file_rejected` [passed / failed]. Output: [FILL IN]

**Final decision:** [FILL IN, e.g. "I kept `_reject_duplicate_keys` with `object_pairs_hook` and removed the old `seen_ids` check because ..."]

---

## Learning cycle 2: Can a failed save destroy a valid file?

**Question I asked:** My assignment asks, "How would you test that a failed save does not overwrite a valid file?" If `open(path, "w")` empties the file before `json.dump` fails, what is left on disk?

**My prediction (write this BEFORE running the experiment):** [FILL IN]

**AI explanation (in my own words):** Opening a file in `"w"` mode erases its contents immediately. If `json.dump` then fails halfway, the old good data is already gone. The safer way is to write the new data to a temporary file and only call `os.replace(temp_path, path)` after the write has fully succeeded. If anything fails first, the real file is never touched, and the temp file is deleted.

**My own experiment:** I saved one valid request, then added something JSON cannot store (a Python `set`) and tried to save again, and compared the file before and after:

```
python3 -c "
from campus_access import registration as r
r.create_request('F001', 'student')
r.save_requests('exp.json')
before = open('exp.json').read()
r.requests['A002'] = {1, 2}
try:
    r.save_requests('exp.json')
except TypeError as e:
    print('save failed:', e)
print('file unchanged:', open('exp.json').read() == before)
"
rm exp.json
```

Result I saw: [FILL IN]

**Verification:** The test `test_failed_save_does_not_overwrite_valid_file` [passed / failed]. [FILL IN anything else you checked]

**Final decision:** [FILL IN, e.g. "I kept the temp-file approach in `save_requests` because ..."]

---

## Optional learning cycle 3: Why `isdigit()` is not enough for ID checks

**Question I asked:** My assignment says to accept only ASCII digits 0-9 in request IDs. Does `isdigit()` alone do that?

**My prediction:** [FILL IN]

**My own experiment:**

```
python3 -c "s = 'A١٢٣'; print(s[1:].isdigit(), s[1:].isascii())"
```

Result I saw: [FILL IN]

**What I learned and decided:** [FILL IN, e.g. "`isdigit()` accepts Arabic-Indic digits, so I also check `isascii()` in `validate_request_id`."]

---

## Reflection (from the assignment)

- Which validation bug surprised me? [FILL IN]
- What did my partner notice during review? [FILL IN after the PR review]
- What can I now explain without AI? [FILL IN]
- What AI advice did I verify, adjust or reject? [FILL IN]
- What would I improve with another day? [FILL IN]
