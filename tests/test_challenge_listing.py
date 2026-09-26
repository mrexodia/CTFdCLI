import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from ctfdcli.commands import challenges as challenges_command
from ctfdcli.core.models import Challenge
from ctfdcli.main import app


class ChallengeListingTests(unittest.TestCase):
    def setUp(self):
        self.profile = SimpleNamespace(
            url="https://ctf.example/",
            token="token",
        )
        self.config_manager = Mock()
        self.config_manager.get_profile.return_value = self.profile

        self.client = Mock()
        self.client.test_connection.return_value = True
        self.client.get_ctf_info.return_value = SimpleNamespace(name="Test CTF")
        self.client.get_challenge_solvers.side_effect = RuntimeError("user mode")
        self.client.get_challenges.return_value = [
            Challenge(
                id=1,
                name="Visible",
                description="Available challenge",
                category="reverse",
                value=100,
            ),
            Challenge(
                id=2,
                name="???",
                description="",
                category="???",
                value=0,
                type="hidden",
            ),
        ]

    def invoke_challenges(self, *arguments):
        runner = CliRunner()
        with patch.object(
            challenges_command,
            "ConfigManager",
            return_value=self.config_manager,
        ):
            with patch.object(
                challenges_command,
                "CTFdClient",
                return_value=self.client,
            ):
                return runner.invoke(app, ["challenges", "list", *arguments])

    def test_challenge_list_hides_locked_placeholders_by_default(self):
        result = self.invoke_challenges()

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Visible", result.output)
        self.assertNotIn("???", result.output)
        self.assertIn("1 locked", result.output)

    def test_challenge_list_can_include_locked_placeholders(self):
        result = self.invoke_challenges("--include-locked")

        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("???", result.output)


if __name__ == "__main__":
    unittest.main()
