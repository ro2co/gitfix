import re
from playwright.sync_api import sync_playwright
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
        """Create a pull request using browser automation."""
        print(f"Opening PR page: {self.github_url}/compare...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                executable_path="/Users/v1wsfuhuan/Library/Caches/ms-playwright/chromium-1148/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
            )
            
            # Check if authentication state exists
            if os.path.exists(self.storage_state_path):
                print("Loading saved authentication state...")
                context = browser.new_context(storage_state=self.storage_state_path)
            else:
                print("No saved authentication state found.")
                context = browser.new_context()
                print("Please login to GitHub in the opened browser.")
                print("After login, the authentication will be saved for future use.")
            
            page = context.new_page()
            
            try:
                # Navigate to the new PR page
                compare_url = f"{self.github_url}/compare"
                page.goto(compare_url)
                
                print("Waiting for page to load...")
                page.wait_for_selector("body")
                
                # If this is the first login, save the authentication state
                if not os.path.exists(self.storage_state_path):
                    print("Waiting for login... (Press Enter when done)")
                    input()
                    # Save authentication state
                    context.storage_state(path=self.storage_state_path)
                    print(f"Authentication state saved at {self.storage_state_path}")
                
                # Let the user handle the rest manually
                print("Browser opened for PR creation. Please complete the process manually.")
                print("Press Enter when done...")
                input()
                
            except Exception as e:
                raise Exception(f"Failed to open PR page: {str(e)}")
            finally:
                browser.close()
