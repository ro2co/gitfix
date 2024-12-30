import subprocess
from typing import List, Optional

class GitOperations:
    """Class to handle all git related operations."""
    
    def _run_command(self, command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """Run a git command and return the result."""
        try:
            result = subprocess.run(
                command,
                check=check,
                capture_output=True,
                text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git command failed: {e.stderr}")

    def create_and_checkout_branch(self, branch_name: str) -> None:
        """Create and checkout a new branch."""
        try:
            self._run_command(['git', 'checkout', '-b', branch_name])
            print(f"✓ Created and checked out branch: {branch_name}")
        except Exception as e:
            raise Exception(f"Failed to create branch: {str(e)}")

    def commit_changes(self, message: str) -> None:
        """Commit changes with the given message."""
        try:
            # First add all changes
            self._run_command(['git', 'add', '.'])
            # Then commit
            self._run_command(['git', 'commit', '-m', message])
            print(f"✓ Committed changes with message: {message}")
        except Exception as e:
            raise Exception(f"Failed to commit changes: {str(e)}")

    def push_branch(self, branch_name: str) -> None:
        """Push the branch to origin."""
        try:
            self._run_command(['git', 'push', 'origin', branch_name])
            print(f"✓ Pushed branch to origin: {branch_name}")
        except Exception as e:
            raise Exception(f"Failed to push branch: {str(e)}")
