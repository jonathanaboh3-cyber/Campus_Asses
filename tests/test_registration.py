import json
import os
import tempfile
import unittest
from campus_access import registration


class TestRegistration(unittest.TestCase):
    def setUp(self):
        # Reset the module's shared state so every test starts clean
        registration.requests = {}
        registration.next_id = 1

        # Use a temporary file so tests never touch your real requests.json
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.path = os.path.join(temp_dir.name, "requests.json")

    def test_create_valid_request(self):
        request = registration.create_request("F001", "visitor")

        self.assertEqual(
            request,
            {
                "id": "A001",
                "fellow_id": "F001",
                "card_type": "visitor",
                "status": "requested",
                "approved_by": None,
            },
        )

    def test_blank_fellow_id_rejected_and_nothing_stored(self):
        with self.assertRaises(ValueError):
            registration.create_request("   ", "student")

        self.assertEqual(registration.requests, {})
        self.assertEqual(registration.next_id, 1)

    def test_invalid_card_type_rejected(self):
        with self.assertRaises(ValueError):
            registration.create_request("F001", "admin")

    def test_malformed_request_id_rejected(self):
        for bad_id in ["B001", "A1", "A00", "A١٢٣", 1]:
            with self.subTest(bad_id=bad_id):
                with self.assertRaises(ValueError):
                    registration.get_request(bad_id)

    def test_ids_stay_unique_after_reload(self):
        registration.create_request("F001", "student")
        registration.save_requests(self.path)

        # Simulate restarting the program
        registration.requests = {}
        registration.next_id = 1
        registration.load_requests(self.path)

        second = registration.create_request("F002", "staff")
        self.assertEqual(second["id"], "A002")

    def test_corrupted_json_rejected_and_records_kept(self):
        registration.create_request("F001", "student")
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{this is not valid json")

        with self.assertRaises(ValueError):
            registration.load_requests(self.path)

        self.assertIn("A001", registration.requests)

    def test_duplicate_ids_in_file_rejected(self):
        record = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }
        text = '{"A001": %s, "A001": %s}' % (json.dumps(record), json.dumps(record))
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(text)

        with self.assertRaises(ValueError):
            registration.load_requests(self.path)

    def test_failed_save_does_not_overwrite_valid_file(self):
        registration.create_request("F001", "student")
        registration.save_requests(self.path)
        with open(self.path, encoding="utf-8") as file:
            good_content = file.read()

        # A set cannot be written as JSON, so this save must fail
        registration.requests["A002"] = {1, 2}
        with self.assertRaises(TypeError):
            registration.save_requests(self.path)

        with open(self.path, encoding="utf-8") as file:
            self.assertEqual(file.read(), good_content)


if __name__ == "__main__":
    unittest.main()