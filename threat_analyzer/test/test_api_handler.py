import unittest
from unittest.mock import patch
from threat_analyzer.api_handler import APIHandler
from google.cloud import webrisk_v1

class TestAPIHandler(unittest.TestCase):

    @patch("google.oauth2.service_account.Credentials.from_service_account_file")
    def setUp(self, mock_credentials):
        # Mock the credentials to prevent file loading
        mock_credentials.return_value = "fake-creds"

        # safe to initialize without real key.json
        self.api_handler = APIHandler()

    def test_threat_types_configured(self):
        # the list of threat types matches expected
        expected_types = [
            webrisk_v1.ThreatType.MALWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING,
            webrisk_v1.ThreatType.UNWANTED_SOFTWARE,
            webrisk_v1.ThreatType.SOCIAL_ENGINEERING_EXTENDED_COVERAGE,
        ]
        self.assertListEqual(self.api_handler.THREAT_TYPE, expected_types)

if __name__ == "__main__":
    unittest.main()
