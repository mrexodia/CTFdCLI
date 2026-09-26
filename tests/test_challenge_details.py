import unittest

from ctfdcli.commands import challenges as challenges_command


class ChallengeDetailTests(unittest.TestCase):
    def test_attachment_name_hides_signed_query_string(self):
        name = challenges_command._attachment_name(
            "https://ctf.example/files/hash/challenge%20file.zip?token=secret"
        )

        self.assertEqual(name, "challenge file.zip")


if __name__ == "__main__":
    unittest.main()
