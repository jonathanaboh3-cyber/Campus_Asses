import os
import tempfile
import unittest

from campus_access import registration
from campus_access.workflow import (
    approve_request,
    issue_request,
    return_card,
)


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        path = os.path.join(self.temp_dir.name, "requests.json")
        registration.load_requests(path)
        self.request = registration.create_request("F001", "student")
        self.request_id = self.request["id"]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_approve_request(self):
        request = approve_request(self.request_id, "Manager A")

        self.assertEqual(request["status"], "approved")
        self.assertEqual(request["approved_by"], "Manager A")

    def test_blank_approver_is_rejected_without_changes(self):
        before = self.request.copy()

        with self.assertRaises(ValueError):
            approve_request(self.request_id, "   ")

        self.assertEqual(self.request, before)

    def test_cannot_issue_unapproved_request(self):
        before = self.request.copy()

        with self.assertRaises(ValueError):
            issue_request(self.request_id)

        self.assertEqual(self.request, before)

    def test_issue_approved_request(self):
        approve_request(self.request_id, "Manager A")

        request = issue_request(self.request_id)

        self.assertEqual(request["status"], "issued")
        self.assertEqual(request["approved_by"], "Manager A")

    def test_return_issued_card(self):
        approve_request(self.request_id, "Manager A")
        issue_request(self.request_id)

        request = return_card(self.request_id)

        self.assertEqual(request["status"], "returned")

    def test_cannot_reissue_returned_card(self):
        approve_request(self.request_id, "Manager A")
        issue_request(self.request_id)
        return_card(self.request_id)
        before = self.request.copy()

        with self.assertRaises(ValueError):
            issue_request(self.request_id)

        self.assertEqual(self.request, before)

    def test_cannot_return_card_that_was_not_issued(self):
        before = self.request.copy()

        with self.assertRaises(ValueError):
            return_card(self.request_id)

        self.assertEqual(self.request, before)


if __name__ == "__main__":
    unittest.main()
