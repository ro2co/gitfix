#!/usr/bin/env python3

import argparse
import subprocess
import sys
from typing import Optional
from .git_operations import GitOperations
from .pr_operations import PROperations

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Git automation tool for creating branches, commits, and PRs')
    parser.add_argument('-b', '--branch', required=True, help='Branch name')
    parser.add_argument('-m', '--message', required=True, help='Commit message')
    return parser.parse_args()

def main() -> None:
    """Main entry point for the gitfix command."""
    try:
        args = parse_arguments()
        
        # Initialize git operations
        git_ops = GitOperations()
        
        # Execute git flow
        # git_ops.create_and_checkout_branch(args.branch)
        # git_ops.commit_changes(args.message)
        # git_ops.push_branch(args.branch)
        
        # Create PR
        pr_ops = PROperations()
        pr_ops.create_pull_request(args.branch, args.message)
        
        print("✨ All operations completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()