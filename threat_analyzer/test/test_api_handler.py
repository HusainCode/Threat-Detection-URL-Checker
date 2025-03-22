import unittest

from threat_analyzer import api_handler
from unittest.mock import patch, MagicMock

from threat_analyzer.api_handler import APIHandler


class TestAPIHandler(unittest.TestCase):


    @patch("threat_analyzer.api_handler.webrisk_v1.WebRiskServiceClient.search_uris")
    def test_api_call(self, mock_search_uris):
        mock_response = MagicMock()
        mock_response.threat.threat_types = APIHandler().get_threat_types
        mock_search_uris.return_value = mock_response

        # I STOPPED HERE


if __name__ == '__main__':
    unittest.main()
