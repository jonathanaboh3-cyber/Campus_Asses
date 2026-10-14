
import unittest

from campus_access.service import create_request


class TestCreateRequest(unittest.TestCase):
    def test_create_valid_request(self):
        request = create_request("A001", "F001", "student")

        self.assertEqual(request["id"], "A001")
        self.assertEqual(request["fellow_id"], "F001")
        self.assertEqual(request["card_type"], "student")
        self.assertEqual(request["status"], "requested")
        self.assertIsNone(request["approved_by"])

    def test_blank_fellow_id_is_rejected(self):
        with self.assertRaises(ValueError):
            create_request("A001", "   ", "student")

    def test_invalid_card_type_is_rejected(self):
        with self.assertRaises(ValueError):
            create_request("A001", "F001", "vip")


if __name__ == "__main__":
    unittest.main()
