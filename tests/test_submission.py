import unittest
from unittest.mock import Mock, patch

from ctfdcli.core.api_client import CTFdClient


class SubmissionTests(unittest.TestCase):
    def test_submit_flag_does_not_print_flag_payload(self):
        client = CTFdClient("https://ctf.example", "token")
        client.console = Mock()

        with patch.object(
            client,
            "_make_request",
            return_value={"status": "correct", "message": "Correct"},
        ):
            accepted, message = client.submit_flag(1, "secret@flare-on.com")

        self.assertTrue(accepted)
        self.assertEqual(message, "Correct")
        client.console.print.assert_not_called()


if __name__ == "__main__":
    unittest.main()
