
ALLOWED_CARD_TYPES = ("visitor", "student", "staff")


def create_request(request_id, fellow_id, card_type):
    if not fellow_id.strip():
        raise ValueError("Fellow ID cannot be empty.")

    if card_type not in ALLOWED_CARD_TYPES:
        raise ValueError("Invalid card type.")

    request = {
        "id": request_id,
        "fellow_id": fellow_id,
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }

    return request
