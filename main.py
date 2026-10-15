from campus_access.registration import (
    create_request,
    get_request,
    save_requests,
    load_requests,
)


def main():
    load_requests()

    first_request = create_request("F001", "student")
    print("Created request:", first_request)

    print("Retrieved request:", get_request(first_request["id"]))

    save_requests()
    print("Requests saved successfully!")


if __name__ == "__main__":
    main()