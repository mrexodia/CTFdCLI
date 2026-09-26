import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from ctfdcli.commands import sync as sync_command
from ctfdcli.core.models import Challenge


class SyncFilteringTests(unittest.TestCase):
    def test_sync_excludes_locked_placeholder_challenges(self):
        profile = SimpleNamespace(
            name="test",
            url="https://ctf.example/",
            token="token",
        )
        config_manager = Mock()
        config_manager.get_profile.return_value = profile

        client = Mock()
        client.test_connection.return_value = True
        client.get_ctf_info.return_value = SimpleNamespace(name="Test CTF")
        client.get_challenges.return_value = [
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

        with tempfile.TemporaryDirectory() as directory:
            with patch.object(
                sync_command,
                "ConfigManager",
                return_value=config_manager,
            ):
                with patch.object(
                    sync_command,
                    "CTFdClient",
                    return_value=client,
                ):
                    sync_command.sync_challenges(
                        profile=None,
                        category=None,
                        output_dir=directory,
                        download_files=False,
                        create_readme=False,
                        force=True,
                        incremental=False,
                        current=False,
                    )

            root = Path(directory)
            self.assertTrue((root / "reverse" / "Visible").is_dir())
            self.assertFalse((root / "???" / "???").exists())


if __name__ == "__main__":
    unittest.main()
