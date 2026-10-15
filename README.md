# Campus_Assess

A command-line Python app for managing campus access-card requests. It uses only the Python standard library.

A request moves through a fixed workflow and is saved to a JSON file, so the data survives a restart.

```
requested -> approved -> issued -> returned
```

- Only a request with a nonempty `approved_by` can be issued.
- States cannot be skipped, and `returned` is final.
- Invalid input (blank fellow ID, unknown card type, malformed or unknown ID, empty approver) is rejected, and a rejected action leaves the record unchanged.

Each request has five fields: `id` (A001, A002 ...), `fellow_id`, `card_type` (visitor, student or staff), `status` and `approved_by`.

## Project structure

```
main.py                     entry point
campus_access/
    registration.py        Engineer A: create, view, validate, save and load requests
    workflow.py            Engineer B: approve, issue and return rules
tests/                      unit tests
docs/
    design-decisions.md    design choices
    ai-learning-log.md     AI learning log
```

## Run

Requires Python 3.12 or newer. From the project folder:

```
python3 main.py
```

## Test

```
python3 -m unittest discover -s tests -v
```

## Team

- Engineer A: registration and data safety (`registration.py`)
- Engineer B: approval and safe workflow (`workflow.py`)

Request IDs stay unique across restarts, and a corrupted or invalid JSON file is rejected with a clear error instead of being replaced with empty data.