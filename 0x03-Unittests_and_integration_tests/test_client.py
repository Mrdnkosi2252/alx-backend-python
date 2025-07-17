
"""Test module for client.GithubOrgClient class."""

import unittest
from client import GithubOrgClient
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from typing import Dict, List

class TestGithubOrgClient(unittest.TestCase):
    """Test class for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_payload: Dict, mock_get_json) -> None:
        """Test that GithubOrgClient.org returns the mocked payload and calls get_json once.

        Args:
            org_name (str): The organization name to test.
            mock_payload (Dict): The expected JSON payload to return from get_json.
            mock_get_json: Mock object for get_json function.
        """
        mock_get_json.return_value = mock_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, mock_payload)

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the expected repos_url from the mocked org payload.

        The test mocks GithubOrgClient.org to return a known payload and verifies
        that _public_repos_url extracts the repos_url correctly.
        """
        with patch.object(GithubOrgClient, 'org', new_callable=property, return_value={"repos_url": "https://api.github.com/orgs/test/repos"}):
            client = GithubOrgClient("test")
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/test/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """Test that public_repos returns the expected list of repo names from the mocked payload.

        The test mocks get_json to return a list of repositories and _public_repos_url
        to provide the URL, verifying the method extracts repo names correctly.
        """
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_url = "https://api.github.com/orgs/test/repos"
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=property, return_value=mock_url):
            mock_get_json.return_value = mock_repos_payload
            client = GithubOrgClient("test")
            result = client.public_repos
            mock_get_json.assert_called_once_with(mock_url)
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """Test that has_license returns the expected boolean based on license key match.

        Args:
            repo (Dict): The repository dictionary containing license information.
            license_key (str): The license key to check against.
            expected (bool): The expected return value (True if keys match, False otherwise).
        """
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        'org_payload': {'repos_url': 'https://api.github.com/orgs/google/repos'},
        'repos_payload': [{'name': 'repo1'}, {'name': 'repo2'}],
        'expected_repos': ['repo1', 'repo2'],
        'apache2_repos': ['repo1']
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient.public_repos method."""

    def setUpClass(cls) -> None:
        """Set up class-level mock for requests.get with fixture-based side effects."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.return_value.json.side_effect = lambda url: cls.org_payload if 'orgs' in url else cls.repos_payload

    def tearDownClass(cls) -> None:
        """Tear down class-level mock by stopping the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns the expected list of repository names.

        The test uses fixture data to verify the integration of public_repos
        with mocked external requests.
        """
        client = GithubOrgClient("google")
        result = client.public_repos
        self.assertEqual(result, self.expected_repos)
        self.mock_get.assert_called()
        self.assertEqual(self.mock_get.call_count, 2)  