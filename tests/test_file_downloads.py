import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from ctfdcli.core.api_client import CTFdClient


class FileDownloadTests(unittest.TestCase):
    def setUp(self):
        self.client = CTFdClient("https://ctf.example", "token")

    def test_get_challenge_files_normalizes_supported_url_forms(self):
        files = [
            "/files/hash/one.bin?token=one",
            "hash/two.bin?token=two",
            "https://cdn.example/three.bin",
        ]

        with patch.object(
            self.client,
            "_make_request",
            return_value={"files": files},
        ):
            urls = self.client.get_challenge_files(1)

        self.assertEqual(
            urls,
            [
                "https://ctf.example/files/hash/one.bin?token=one",
                "https://ctf.example/files/hash/two.bin?token=two",
                "https://cdn.example/three.bin",
            ],
        )

    def test_download_file_accepts_relative_ctfd_url(self):
        response = Mock()
        response.iter_content.return_value = [b"first", b"second"]
        self.client.session.get = Mock(return_value=response)

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "attachment.bin"
            downloaded = self.client.download_file(
                "/files/hash/attachment.bin?token=secret",
                str(destination),
            )

            self.assertTrue(downloaded)
            self.assertEqual(destination.read_bytes(), b"firstsecond")

        self.client.session.get.assert_called_once_with(
            "https://ctf.example/files/hash/attachment.bin?token=secret",
            stream=True,
            timeout=30,
        )
        response.raise_for_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
