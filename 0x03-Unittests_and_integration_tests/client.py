#!/usr/bin/env python3
"""Client module for interacting with GitHub organization data."""

from typing import Dict
import requests


def get_json(url: str) -> Dict:
    """Fetch JSON data from a given URL."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Client for GitHub organization operations."""

    def __init__(self, org_name: str) -> None:
        """Initialize with the organization name."""
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Fetches the public metadata of the GitHub organization for this client instance."""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Returns the URL for the organization's public repositories."""
        return self.org.get("repos_url")

    def public_repos(self) -> list:
        """Returns a list of public repository names."""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    def has_license(self, repo: Dict, license_key: str) -> bool:
        """Checks if a repository has the specified license."""
        return repo.get("license", {}).get("key") == license_key
