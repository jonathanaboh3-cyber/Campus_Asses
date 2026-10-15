# Design Decisions: Campus Access

> Written by Engineer A from the actual behaviour of `campus_access/registration.py`. Lines marked **[CONFIRM WITH B]** need Engineer B's agreement before you submit. Replace the marker with the agreed text.

## 1. What does one request dictionary look like?

Every request is one dictionary with exactly five fields:

```python
{
    "id": "A001",
    "fellow_id": "F001",
    "card_type": "student",     # visitor, student or staff
    "status": "requested",      # requested, approved, issued or returned
    "approved_by": None         # None until approved, then a nonempty string
}
```

All requests are stored in one dictionary called `requests`, where the key is the request ID. This allows a direct lookup by ID without searching a list, and it keeps the ID in one place. Saved as JSON, `None` becomes `null`.

## 2. What should `create_request` return?

It returns the new request dictionary (all five fields). The caller can show it or check it straight away, and it is the same record stored in `requests`.

## 3. How will functions report invalid inputs?

Every function raises `ValueError` with a clear message, for example "Fellow ID cannot be blank" or "Invalid card type". Validation happens BEFORE anything is written, so a rejected call leaves no partial record and does not use up an ID. The menu code (Engineer B's `run_menu`) catches `ValueError` and shows the message instead of crashing. **[CONFIRM WITH B]**

## 4. Where is the next ID generated?

Only in `registration.py`, by the module variable `next_id`. The format is `A` plus three digits (`A001`, `A002` ...). When data is loaded from JSON, `next_id` is set to the highest number found plus one, so IDs stay unique across restarts. If the file is missing or has no records, it starts at 1. The limit is `A999`, after which creating a request raises `ValueError`. Only ASCII digits 0-9 are accepted in IDs.

## 5. How will Engineer B call Engineer A's storage functions?

Engineer B imports the module and calls its four public functions:

```python
from campus_access import registration

registration.create_request(fellow_id, card_type)
registration.get_request(request_id)
registration.save_requests(path)
registration.load_requests(path)
```

Rule: B must not edit `registration.requests` or `registration.next_id` directly and must not write its own JSON code. **[CONFIRM WITH B]**

Open point: `get_request` currently returns the stored record itself, so B changes `status` and `approved_by` on that record. B must check that the transition is legal BEFORE changing anything, so a rejected action leaves the record exactly as it was. **[CONFIRM WITH B: either keep this rule, or agree that A adds a function such as `update_request` that B calls instead.]**

## 6. What happens if a saved JSON file is invalid?

`load_requests` raises `ValueError` with a clear message and changes nothing: the records already in memory stay, and the file on disk is never replaced with empty data. It rejects:

- text that is not valid JSON, including an empty file
- a file whose top level is not a dictionary
- duplicate keys
- missing or extra fields in a request
- a request ID that does not match its key, or is badly formatted
- an invalid fellow ID, card type or status
- a "requested" record that has an approver, or an approved/issued/returned record with no approver

The only exception is a file that does not exist yet: that means "no saved data", so the program starts with an empty list.

## 7. Which data must never change on a rejected operation?

- The `requests` dictionary and every record inside it
- The `next_id` counter (a rejected create does not use up an ID)
- The saved JSON file on disk. `save_requests` writes to a temporary file first and only then replaces the real file, so a failed save keeps the old valid file.

## Workflow rules (Engineer B to complete)

The allowed order is requested -> approved -> issued -> returned. Skipping a state is rejected, "returned" is final, and a card can be issued only when `approved_by` is nonempty. **[B: add how `workflow.py` enforces this and how a rejected action leaves the record unchanged.]**
