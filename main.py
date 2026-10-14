
def validate_fellow_id(fellow_id):
    if not isinstance(fellow_id, str):
        raise ValueError("Fellow ID must be a string")

    if not fellow_id.strip():
        raise ValueError("Fellow ID cannot be blank")


def validate_card_type(card_type):
    allowed_types = {"visitor", "student", "staff"}

    if not isinstance(card_type, str):
        raise ValueError("Card type must be a string")

    if card_type not in allowed_types:
        raise ValueError("Invalid card type")


# Stores all requests
requests = {}

# Counter for generating request IDs
next_id = 1


def create_request(fellow_id, card_type):
    global next_id

    # Validate the inputs
    validate_fellow_id(fellow_id)
    validate_card_type(card_type)

    # Generate a unique request ID
    request_id = f"A{next_id:03d}"
    next_id += 1

    # Create the request with five required fields
    request = {
        "id": request_id,
        "fellow_id": fellow_id,
        "card_type": card_type,
        "status": "requested",
        "approved_by": ""
    }

    # Store the request
    requests[request_id] = request

    # Return the created request
    return request


# Temporary tests for validate_fellow_id()

validate_fellow_id("F001")
print("Valid ID accepted!")

try:
    validate_fellow_id("   ")
except ValueError as error:
    print("Invalid ID rejected:", error)

try:
    validate_fellow_id(123)
except ValueError as error:
    print("Wrong input type rejected:", error)


# Temporary tests for validate_card_type()

validate_card_type("visitor")
print("Valid card type accepted!")

try:
    validate_card_type("guest")
except ValueError as error:
    print("Invalid card type rejected:", error)

try:
    validate_card_type(123)
except ValueError as error:
    print("Wrong input type rejected:", error)
