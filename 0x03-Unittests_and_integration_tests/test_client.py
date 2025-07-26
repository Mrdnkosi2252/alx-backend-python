#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("utils.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that .org returns correct data."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch(
        "client.GithubOrgClient.org",
        return_value={"repos_url": "https://api.github.com/orgs/google/repos"}
    )
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns correct URL."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/google/repos"
        )

    @patch("utils.get_json", return_value=[
        {"name": "repo1"},
        {"name": "repo2"}
    ])
    @patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock
    )
    def test_public_repos(self, mock_url, mock_get_json):
        """Test that public_repos returns correct repo names."""
        mock_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_get_json.assert_called_once_with(mock_url.return_value)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Start patcher and set side effects for requests.get().json()."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by license correctly."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
