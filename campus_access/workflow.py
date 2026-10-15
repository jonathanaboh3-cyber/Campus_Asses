from campus_access import registration


def approve_request(request_id, approver):
    """Approve a request that is still awaiting approval."""
    if not isinstance(approver, str) or not approver.strip():
        raise ValueError("Approver cannot be empty.")

    request = registration.get_request(request_id)

    if request["status"] != "requested":
        raise ValueError("Only requested cards can be approved.")

    request["approved_by"] = approver.strip()
    request["status"] = "approved"
    return request


def issue_request(request_id):
    """Issue a card only after valid approval."""
    request = registration.get_request(request_id)

    if request["status"] != "approved":
        raise ValueError("Only approved cards can be issued.")

    approver = request["approved_by"]
    if not isinstance(approver, str) or not approver.strip():
        raise ValueError("A valid approver is required to issue a card.")

    request["status"] = "issued"
    return request


def return_card(request_id):
    """Mark an issued card as returned."""
    request = registration.get_request(request_id)

    if request["status"] != "issued":
        raise ValueError("Only issued cards can be returned.")

    request["status"] = "returned"
    return request
