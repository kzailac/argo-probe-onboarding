import unittest

from argo_probe_onboarding.status import Status


class StatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.status = Status()

    def test_default(self):
        self.assertEqual(self.status.status_code, 0)
        self.assertEqual(self.status.status_msg, "OK")

    def test_ok_msg(self):
        self.status.ok("Some new OK message")
        self.assertEqual(self.status.status_code, 0)
        self.assertEqual(self.status.status_msg, "OK - Some new OK message")

    def test_warning_msg(self):
        self.status.warning("You have been warned")
        self.assertEqual(self.status.status_code, 1)
        self.assertEqual(
            self.status.status_msg, "WARNING - You have been warned"
        )

    def test_critical_msg(self):
        self.status.critical(
            "Listen to me carefully, I shall say this only once"
        )
        self.assertEqual(self.status.status_code, 2)
        self.assertEqual(
            self.status.status_msg,
            "CRITICAL - Listen to me carefully, I shall say this only once"
        )

    def test_unknown_msg(self):
        self.status.unknown("The great unknown")
        self.assertEqual(self.status.status_code, 3)
        self.assertEqual(self.status.status_msg, "UNKNOWN - The great unknown")
