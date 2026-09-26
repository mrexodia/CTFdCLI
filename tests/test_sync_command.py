import unittest
from unittest.mock import patch

from typer.main import get_command
from typer.testing import CliRunner

from ctfdcli.commands import sync as sync_command
from ctfdcli.main import app


class SyncCommandTests(unittest.TestCase):
    def test_bare_sync_runs_default_action_with_group_options(self):
        runner = CliRunner()

        with patch.object(sync_command, "sync_challenges") as sync_challenges:
            result = runner.invoke(
                app,
                [
                    "sync",
                    "--output",
                    "destination",
                    "--no-files",
                    "--no-readme",
                    "--force",
                    "--full",
                ],
            )

        self.assertEqual(result.exit_code, 0, result.output)
        sync_challenges.assert_called_once_with(
            profile=None,
            category=None,
            output_dir="destination",
            download_files=False,
            create_readme=False,
            force=True,
            incremental=False,
            current=False,
        )

    def test_sync_group_only_lists_status_subcommand(self):
        command = get_command(sync_command.app)

        self.assertEqual(set(command.commands), {"status"})



if __name__ == "__main__":
    unittest.main()
