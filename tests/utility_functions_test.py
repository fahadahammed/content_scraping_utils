import unittest
from unittest.mock import patch, MagicMock, Mock, DEFAULT
from requests.exceptions import Timeout
from src.utility_functions import the_requester, article_file_exists, list_files_in_directory


class TestUtility(unittest.TestCase):
    @patch('requests.get')
    def test_invalid_url(self, mock_requests_get):
        # Mock the requests.get function to simulate an invalid URL
        mock_response = MagicMock()
        mock_response.status_code = 404  # Set status code to simulate an invalid URL
        mock_requests_get.return_value = mock_response

        # Call the function with an invalid URL
        result = the_requester('http://example.invalid')

        # Assert that the function returns False for an invalid URL
        self.assertFalse(result)

    @patch('requests.get')
    def test_timeout(self, mock_requests_get):
        mock_requests_get.side_effect = Timeout

        result = the_requester('http://example.com')

        self.assertFalse(result)

    @patch('src.utility_functions.list_files_in_directory')
    def test_article_file_exists(self, mock_list_files):
        # Mock the list_files_in_directory function to return a list of files
        mock_list_files.return_value = ['file1', 'file2', 'file3']

        # Test when the file does not exist
        self.assertFalse(article_file_exists('file4'))

        # Test when the file exists
        self.assertTrue(article_file_exists('file2'))


if __name__ == '__main__':
    unittest.main()