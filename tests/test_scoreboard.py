import unittest
from unittest.mock import patch

from ctfdcli.core.api_client import CTFdClient


class ScoreboardTests(unittest.TestCase):
    def test_get_scoreboard_enforces_count_when_server_ignores_it(self):
        client = CTFdClient("https://ctf.example", "token")
        response = [
            {"account_id": index, "name": f"player-{index}", "score": 100 - index}
            for index in range(5)
        ]

        with patch.object(
            client,
            "_make_request",
            return_value=response,
        ) as request:
            entries = client.get_scoreboard(2)

        self.assertEqual(
            [entry.account_name for entry in entries],
            ["player-0", "player-1"],
        )
        request.assert_called_once_with("GET", "/scoreboard?count=2")


if __name__ == "__main__":
    unittest.main()
