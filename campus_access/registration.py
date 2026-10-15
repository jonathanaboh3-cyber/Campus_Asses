import json
import os

# Stores all requests, keyed by request ID
requests = {}

# Counter for generating request IDs
next_id = 1

ALLOWED_CARD_TYPES = {"visitor", "student", "staff"}
ALLOWED_STATUSES = {"requested", "approved", "issued", "returned"}
REQUIRED_FIELDS = {"id", "fellow_id", "card_type", "status", "approved_by"}
MAX_ID_NUMBER = 999


def validate_fellow_id(fellow_id):
    if not isinstance(fellow_id, str):
        raise ValueError("Fellow ID must be a string")

    if not fellow_id.strip():
        raise ValueError("Fellow ID cannot be blank")


def validate_card_type(card_type):
    if not isinstance(card_type, str):
        raise ValueError("Card type must be a string")

    if card_type not in ALLOWED_CARD_TYPES:
        raise ValueError("Invalid card type")


def validate_request_id(request_id):
    if not isinstance(request_id, str):
        raise ValueError("Request ID must be a string")

    if (
        len(request_id) != 4
        or request_id[0] != "A"
        or not request_id[1:].isascii()
        or not request_id[1:].isdigit()
        or int(request_id[1:]) < 1
    ):
        raise ValueError("Invalid request ID format")


def create_request(fellow_id, card_type):
    global next_id

    validate_fellow_id(fellow_id)
    validate_card_type(card_type)

    if next_id > MAX_ID_NUMBER:
        raise ValueError("Request ID limit reached")

    while f"A{next_id:03d}" in requests:
        next_id += 1

    if next_id > MAX_ID_NUMBER:
        raise ValueError("Request ID limit reached")

    request_id = f"A{next_id:03d}"
    next_id += 1

    request = {
        "id": request_id,
        "fellow_id": fellow_id,
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }

    requests[request_id] = request

    return request.copy()


def get_request(request_id):
    validate_request_id(request_id)

    if request_id not in requests:
        raise ValueError("Request not found")

    return requests[request_id].copy()


def save_requests(path="requests.json"):
    temp_path = path + ".tmp"

    try:
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(requests, file, indent=4)

        os.replace(temp_path, path)

    except (OSError, TypeError, ValueError):
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


def _reject_duplicate_keys(pairs):
    result = {}

    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate key in file: {key}")

        result[key] = value

    return result


def load_requests(path="requests.json"):
    global requests, next_id

    if not os.path.exists(path):
        requests = {}
        next_id = 1
        return

    try:
        with open(path, "r", encoding="utf-8") as file:
            loaded_requests = json.load(
                file,
                object_pairs_hook=_reject_duplicate_keys,
            )

    except json.JSONDecodeError as error:
        raise ValueError("Invalid JSON file") from error

    except UnicodeDecodeError as error:
        raise ValueError("Invalid file encoding") from error

    if not isinstance(loaded_requests, dict):
        raise ValueError("Requests file must contain a dictionary")

    for request_id, request in loaded_requests.items():
        validate_request_id(request_id)

        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")

        if set(request.keys()) != REQUIRED_FIELDS:
            raise ValueError("Request has missing or unexpected fields")

        if request_id != request["id"]:
            raise ValueError(
                "Request ID does not match its dictionary key"
            )

        validate_fellow_id(request["fellow_id"])
        validate_card_type(request["card_type"])

        status = request["status"]

        if not isinstance(status, str) or status not in ALLOWED_STATUSES:
            raise ValueError("Invalid request status")

        approved_by = request["approved_by"]

        if status == "requested":
            if approved_by is not None:
                raise ValueError(
                    "Requested records cannot have an approver"
                )

        elif (
            not isinstance(approved_by, str)
            or not approved_by.strip()
        ):
            raise ValueError(
                "Approved records must have a valid approver"
            )

    # Replace memory only after all records pass validation
    requests = loaded_requests

    if requests:
        next_id = max(
            int(request_id[1:]) for request_id in requests
        ) + 1
    else:
        next_id = 1