#!/usr/bin/env python3
"""Unit tests for the client module."""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("utils.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data."""
        test_payload = {"login": org_name}

        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), test_payload)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch(
        "client.GithubOrgClient.org",
        return_value={"repos_url": "some_url"}
    )
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property returns correct repos_url."""
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "some_url")

    @patch("utils.get_json", return_value=[
        {"name": "repo1"},
        {"name": "repo2"}
    ])
    @patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=PropertyMock
    )
    def test_public_repos(self, mock_url, mock_get_json):
        """Test public_repos method returns correct list of repo names."""
        mock_url.return_value = "some_url"
        client = GithubOrgClient("google")
        result = client.public_repos()
        expected = ["repo1", "repo2"]
        self.assertEqual(result, expected)
        self.assertEqual(client._public_repos_url, "some_url")
        mock_get_json.assert_called_once_with("some_url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license correctly identifies license match."""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
