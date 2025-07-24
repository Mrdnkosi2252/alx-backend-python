#!/usr/bin/env python3
"""Test module for client.GithubOrgClient class."""

import unittest
from client import GithubOrgClient
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """Test class for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_payload: Dict,
                 mock_get_json) -> None:
        """Test that GithubOrgClient.org returns the mocked payload."""
        mock_get_json.return_value = mock_payload
        client = GithubOrgClient(org_name)
        result = client.org
        expected = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected)
        self.assertEqual(result, mock_payload)

    @patch('client.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url', new_callable=property)
    def test_public_repos(self, mock_url, mock_get_json) -> None:
        """Test that public_repos returns expected repo names."""
        mock_url.return_value = "https://api.github.com/orgs/test/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        client = GithubOrgClient("test")
        result = client.public_repos
        expected = mock_url.return_value
        mock_get_json.assert_called_once_with(expected)
        self.assertEqual(result, ["repo1", "repo2", "repo3"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict,
                         license_key: str,
                         expected: bool) -> None:
        """Test that has_license returns expected boolean outcome."""
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
    """Integration test for GithubOrgClient using fixture-based mocks."""

    @classmethod
    def setUpClass(cls) -> None:
        """Patch requests.get and apply side effect based on URL."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.return_value.json.side_effect = (
            lambda url: cls.org_payload
            if 'orgs' in url else cls.repos_payload
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the patcher after tests."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Verify public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        result = client.public_repos
        self.assertEqual(result, self.expected_repos)
        self.assertEqual(self.mock_get.call_count, 2)
