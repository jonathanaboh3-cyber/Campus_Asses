from campus_access import registration
from campus_access.workflow import (
    approve_request,
    issue_request,
    return_card,
)


def display_request(request):
    print(f"Request ID: {request['id']}")
    print(f"Fellow ID: {request['fellow_id']}")
    print(f"Card type: {request['card_type']}")
    print(f"Status: {request['status']}")
    print(f"Approved by: {request['approved_by']}")


def run_menu():
    while True:
        print("\n=== CAMPUS ACCESS ===")
        print("1. Create request")
        print("2. View request")
        print("3. Approve request")
        print("4. Issue card")
        print("5. Return card")
        print("6. List all requests")
        print("7. Save requests")
        print("8. Reload requests")
        print("9. Quit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                fellow_id = input("Enter fellow ID: ").strip()
                card_type = input(
                    "Enter card type (visitor/student/staff): "
                ).strip().lower()

                request = registration.create_request(
                    fellow_id, card_type
                )
                registration.save_requests()

                print("\nRequest created successfully.")
                display_request(request)

            elif choice == "2":
                request_id = input("Enter request ID: ").strip()
                request = registration.get_request(request_id)
                display_request(request)

            elif choice == "3":
                request_id = input("Enter request ID: ").strip()
                approver = input("Enter approver ID: ").strip()

                request = approve_request(request_id, approver)
                registration.save_requests()

                print("Request approved successfully.")
                display_request(request)

            elif choice == "4":
                request_id = input("Enter request ID: ").strip()

                request = issue_request(request_id)
                registration.save_requests()

                print("Card issued successfully.")
                display_request(request)

            elif choice == "5":
                request_id = input("Enter request ID: ").strip()

                request = return_card(request_id)
                registration.save_requests()

                print("Card returned successfully.")
                display_request(request)

            elif choice == "6":
                if not registration.requests:
                    print("No requests found.")
                else:
                    for request_id in sorted(registration.requests):
                        print()
                        display_request(
                            registration.requests[request_id]
                        )

            elif choice == "7":
                registration.save_requests()
                print("Requests saved successfully.")

            elif choice == "8":
                registration.load_requests()
                print("Requests reloaded successfully.")

            elif choice == "9":
                registration.save_requests()
                print("Requests saved. Goodbye!")
                break

            else:
                print("Invalid option. Choose a number from 1 to 9.")

        except (ValueError, OSError) as error:
            print(f"Operation failed: {error}")


def main():
    try:
        registration.load_requests()
    except (ValueError, OSError) as error:
        print(f"Could not load requests: {error}")
        return

    run_menu()


if __name__ == "__main__":
    main()