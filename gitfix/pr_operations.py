import re
import requests
import os
import time
from typing import Optional, Tuple
from urllib.parse import urlparse

class PROperations:
    """Class to handle GitHub Pull Request operations using Playwright."""
    
    def __init__(self):
        """Initialize PR operations with default values."""
        self.base_branch = "staging"
        self.github_url = self._get_github_url()
        # Initialize storage path with proper directory structure
        self.storage_state_path = os.path.join(os.path.expanduser("~"), ".config", "gitfix", "github_state.json")
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.storage_state_path), exist_ok=True)

    def _get_github_token(self) -> str:
        \"\"\"Get GitHub token from environment variable.\"\"\"
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError(
                \"GITHUB_TOKEN environment variable not set. \"
                \"Please set it with your GitHub personal access token.\"
            )
        return token

    def _parse_git_url(self, url: str) -> Tuple[str, str]:
        """
        Parse git URL to extract username and repository name.
        Supports various git URL formats:
        - ssh://git@ssh.github.com:443/hello/web.git
        - git@github.com:username/repo.git
        - https://github.com/username/repo.git
        """
        url = url.strip()
        
        # Remove .git suffix if present
        if url.endswith('.git'):
            url = url[:-4]

        # Pattern 1: ssh://git@ssh.github.com:443/user/repo
        ssh_pattern = r'ssh://git@(?:ssh\.)?github\.com(?::\d+)?/([^/]+)/(.+)'
        if match := re.match(ssh_pattern, url):
            return match.group(1), match.group(2)

        # Pattern 2: git@github.com:user/repo
        git_pattern = r'git@github\.com:([^/]+)/(.+)'
        if match := re.match(git_pattern, url):
            return match.group(1), match.group(2)

        # Pattern 3: https://github.com/user/repo
        try:
            parsed = urlparse(url)
            if parsed.netloc == 'github.com':
                parts = parsed.path.strip('/').split('/')
                if len(parts) >= 2:
                    return parts[0], parts[1]
        except Exception:
            pass

        raise ValueError(f"Unsupported or invalid git URL format: {url}")

    def _get_github_url(self) -> str:
        """Get GitHub repository URL from git remote."""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                check=True
            )
            url = result.stdout.strip()
            
            # Parse the URL to get username and repo
            username, repo = self._parse_git_url(url)
            
            # Construct GitHub PR URL
            return f"https://github.com/{username}/{repo}"
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to get git remote URL: {str(e)}")
        except ValueError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Failed to process GitHub URL: {str(e)}")

    def create_pull_request(self, branch_name: str, title: str) -> None:
        """
        Create a pull request using GitHub API.
        
        Args:
            branch_name: Name of the source branch
            title: Title for the pull request
        """
        api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls"
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # PR data
        data = {
            "title": title,
            "head": branch_name,
            "base": self.base_branch,
            "body": f"Created by gfix tool Merging from `{branch_name}` into `{self.base_branch}`"
        }
        
        try:
            print(f"Creating PR to merge '{branch_name}' into '{self.base_branch}'...")
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            
            pr_data = response.json()
            print(f"✓ Successfully created PR: {pr_data['html_url']}")
            
        except requests.exceptions.RequestException as e:
            if response := getattr(e, 'response', None):
                error_msg = response.json().get('message', str(e))
                raise Exception(f"Failed to create PR: {error_msg}")
            raise Exception(f"Failed to create PR: {str(e)}")
