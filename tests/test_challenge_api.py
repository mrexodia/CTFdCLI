import unittest
from unittest.mock import patch

from ctfdcli.core.api_client import CTFdAPIError, CTFdClient


class ChallengeAPITests(unittest.TestCase):
    def setUp(self):
        self.client = CTFdClient("https://ctf.example", "token")

    def test_get_challenges_accepts_locked_placeholders(self):
        responses = {
            "/challenges": [
                {
                    "id": 1,
                    "name": "Visible",
                    "category": "re",
                    "value": 100,
                    "solved_by_me": False,
                },
                {
                    "id": 2,
                    "name": "???",
                    "category": "???",
                    "value": 0,
                    "type": "hidden",
                },
            ],
            "/challenges/1": {
                "id": 1,
                "name": "Visible",
                "description": "Challenge description",
                "category": "re",
                "value": 100,
                "attempts": 1,
                "max_attempts": 0,
                "solved_by_me": True,
                "tags": [{"value": "windows"}, {"name": "x64"}],
                "files": ["/files/hash/sample.zip?token=secret"],
            },
            "/challenges/2": {
                "id": 2,
                "name": "???",
                "category": "???",
                "value": 0,
                "type": "hidden",
            },
        }

        with patch.object(
            self.client,
            "_make_request",
            side_effect=lambda method, endpoint: responses[endpoint],
        ):
            challenges = self.client.get_challenges()

        self.assertEqual(len(challenges), 2)
        self.assertEqual(challenges[0].description, "Challenge description")
        self.assertTrue(challenges[0].solved_by_me)
        self.assertEqual(challenges[0].tags, ["windows", "x64"])
        self.assertIsNone(challenges[0].max_attempts)
        self.assertEqual(
            challenges[0].files,
            ["https://ctf.example/files/hash/sample.zip?token=secret"],
        )
        self.assertEqual(challenges[1].description, "")
        self.assertEqual(challenges[1].attempts, 0)

    def test_get_challenges_uses_summary_when_detail_is_unavailable(self):
        summary = {
            "id": 7,
            "name": "Summary only",
            "category": "misc",
            "value": 50,
        }

        def request(method, endpoint):
            if endpoint == "/challenges":
                return [summary]
            raise CTFdAPIError("detail unavailable")

        with patch.object(self.client, "_make_request", side_effect=request):
            challenge = self.client.get_challenges()[0]

        self.assertEqual(challenge.name, "Summary only")
        self.assertEqual(challenge.description, "")
        self.assertEqual(challenge.attempts, 0)


if __name__ == "__main__":
    unittest.main()
