
import utils

class GithubOrgClient:
    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        url = f"https://api.github.com/orgs/{self.org_name}"
        return utils.get_json(url)

    @property
    def _public_repos_url(self):
        return self.org().get("repos_url", "")

    def public_repos(self):
        return [repo["name"] for repo in utils.get_json(self._public_repos_url)]

    def has_license(self, repo, license_key):
        return repo.get("license", {}).get("key") == license_key