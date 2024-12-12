import os
import hashlib
import pickle
from datetime import datetime
import difflib
import shutil
import argparse

# Constants for the VCS system
VCS_DIR = ".myvcs"
INDEX_FILE = "index"
COMMITS_DIR = "commits"
REFS_DIR = "refs"
HEAD_FILE = "HEAD"
GITIGNORE_FILE = ".gitignore"

# Get the current commit hash
def get_current_commit():
    head_path = os.path.join(VCS_DIR, HEAD_FILE)
    if os.path.exists(head_path):
        with open(head_path, 'r') as head_file:
            current_branch = head_file.read().strip()
        branch_path = os.path.join(VCS_DIR, REFS_DIR, current_branch)
        if os.path.exists(branch_path):
            with open(branch_path, 'r') as branch_file:
                return branch_file.read().strip()
    return None

# Utility Functions
def init_repository():
    """Initializes a new repository."""
    if os.path.exists(VCS_DIR):
        print("Repository already initialized.")
        return

    os.makedirs(VCS_DIR)
    os.makedirs(os.path.join(VCS_DIR, COMMITS_DIR))
    os.makedirs(os.path.join(VCS_DIR, REFS_DIR))

    with open(os.path.join(VCS_DIR, INDEX_FILE), 'wb') as index_file:
        pickle.dump({}, index_file)

    with open(os.path.join(VCS_DIR, HEAD_FILE), 'w') as head_file:
        head_file.write("master")

    master_branch = os.path.join(VCS_DIR, REFS_DIR, "master")
    with open(master_branch, 'w') as branch_file:
        branch_file.write("")

    print("Initialized empty repository in .myvcs")

def hash_file(file_path):
    """Calculates the hash of a file."""
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_index():
    """Loads the index from the repository."""
    with open(os.path.join(VCS_DIR, INDEX_FILE), 'rb') as index_file:
        return pickle.load(index_file)

def save_index(index):
    """Saves the index to the repository."""
    with open(os.path.join(VCS_DIR, INDEX_FILE), 'wb') as index_file:
        pickle.dump(index, index_file)

def add_file(file_path):
    """Stages a file for the next commit."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    if file_path in load_gitignore():
        print(f"File {file_path} is ignored by .gitignore.")
        return

    file_hash = hash_file(file_path)
    index = load_index()
    index[file_path] = file_hash
    save_index(index)
    print(f"Staged {file_path}")

def commit(message):
    """Creates a new commit, including file contents."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    index = load_index()
    if not index:
        print("No changes to commit.")
        return

    # Save file content in the commit
    commit_files = {}
    for file_path in index:
        with open(file_path, 'rb') as file:
            commit_files[file_path] = file.read()

    with open(os.path.join(VCS_DIR, HEAD_FILE), 'r') as head_file:
        current_branch = head_file.read().strip()

    branch_path = os.path.join(VCS_DIR, REFS_DIR, current_branch)
    parent_commit = None
    if os.path.exists(branch_path):
        with open(branch_path, 'r') as branch_file:
            parent_commit = branch_file.read().strip()

    commit_data = {
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "parent": parent_commit,
        "files": commit_files
    }

    commit_hash = hashlib.sha1(pickle.dumps(commit_data)).hexdigest()
    commit_path = os.path.join(VCS_DIR, COMMITS_DIR, commit_hash)

    with open(commit_path, 'wb') as commit_file:
        pickle.dump(commit_data, commit_file)

    with open(branch_path, 'w') as branch_file:
        branch_file.write(commit_hash)

    save_index({})
    print(f"Committed changes: {message}")

def log():
    """Displays the commit history."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    with open(os.path.join(VCS_DIR, HEAD_FILE), 'r') as head_file:
        current_branch = head_file.read().strip()

    branch_path = os.path.join(VCS_DIR, REFS_DIR, current_branch)
    if not os.path.exists(branch_path):
        print("No commits yet.")
        return

    commit_hash = open(branch_path).read().strip()
    while commit_hash:
        commit_path = os.path.join(VCS_DIR, COMMITS_DIR, commit_hash)
        with open(commit_path, 'rb') as commit_file:
            commit_data = pickle.load(commit_file)

        print(f"Commit: {commit_hash}")
        print(f"Date: {commit_data['timestamp']}")
        print(f"Message: {commit_data['message']}\n")

        commit_hash = commit_data["parent"]

def create_branch(branch_name):
    """Creates a new branch."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    current_commit = get_current_commit()
    if not current_commit:
        print("No commits to branch from.")
        return

    branch_path = os.path.join(VCS_DIR, REFS_DIR, branch_name)
    if os.path.exists(branch_path):
        print(f"Branch {branch_name} already exists.")
        return

    with open(branch_path, 'w') as branch_file:
        branch_file.write(current_commit)
    print(f"Created branch {branch_name}")

def has_uncommitted_changes():
    """Checks if there are uncommitted changes in the repository."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return False

    # Load the current commit
    current_commit_hash = get_current_commit()
    if current_commit_hash:
        commit_path = os.path.join(VCS_DIR, COMMITS_DIR, current_commit_hash)
        with open(commit_path, 'rb') as commit_file:
            current_commit = pickle.load(commit_file)
    else:
        current_commit = {"files": {}}

    # Compare working directory with the commit
    for file_path, commit_hash in current_commit["files"].items():
        if not os.path.exists(file_path):
            print(f"File {file_path} has been deleted.")
            return True
        if hash_file(file_path) != commit_hash:
            print(f"File {file_path} has been modified.")
            return True

    # Compare working directory with the index
    index = load_index()
    for file_path, staged_hash in index.items():
        if not os.path.exists(file_path):
            print(f"File {file_path} has been deleted.")
            return True
        if hash_file(file_path) != staged_hash:
            print(f"File {file_path} has been modified.")
            return True

    # Check for untracked files
    tracked_files = set(current_commit["files"].keys()).union(index.keys())
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.startswith("."):  # Skip hidden files
                continue
            file_path = os.path.relpath(os.path.join(root, file))
            if file_path not in tracked_files:
                print(f"Untracked file {file_path} found.")
                return True

    print("No uncommitted changes detected.")
    return False

def checkout_branch(branch_name):
    """Switches to the specified branch."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    branch_path = os.path.join(VCS_DIR, REFS_DIR, branch_name)
    if not os.path.exists(branch_path):
        print(f"Branch {branch_name} does not exist.")
        return

    # Check if already on the target branch
    with open(os.path.join(VCS_DIR, HEAD_FILE), 'r') as head_file:
        current_branch = head_file.read().strip()
    if current_branch == branch_name:
        print(f"Already on branch {branch_name}.")
        return

    # Check for uncommitted changes
    if has_uncommitted_changes():
        print("Warning: You have uncommitted changes. Commit them or stash them before switching branches.")
        return

    # Switch to the new branch
    with open(os.path.join(VCS_DIR, HEAD_FILE), 'w') as head_file:
        head_file.write(branch_name)
    print(f"Switched to branch {branch_name}")

def merge_branch(branch_name):
    """Merges the specified branch into the current branch."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    with open(os.path.join(VCS_DIR, HEAD_FILE), 'r') as head_file:
        current_branch = head_file.read().strip()

    branch_path = os.path.join(VCS_DIR, REFS_DIR, branch_name)
    if not os.path.exists(branch_path):
        print(f"Branch {branch_name} does not exist.")
        return

    current_branch_path = os.path.join(VCS_DIR, REFS_DIR, current_branch)
    with open(current_branch_path, 'r') as current_file:
        current_commit = current_file.read().strip()

    with open(branch_path, 'r') as branch_file:
        merge_commit = branch_file.read().strip()

    if current_commit == merge_commit:
        print("Already up to date.")
        return

    print(f"Merged branch {branch_name} into {current_branch}")

def load_gitignore():
    """Loads the .gitignore file."""
    gitignore_path = os.path.join(VCS_DIR, GITIGNORE_FILE)
    ignored_files = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            ignored_files = gitignore_file.read().splitlines()
    return ignored_files

def main():
    parser = argparse.ArgumentParser(description="A simple version control system.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: init
    subparsers.add_parser("init", help="Initialize a new repository.")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Stage a file.")
    add_parser.add_argument("file_path", help="Path of the file to stage.")

    # Command: commit
    commit_parser = subparsers.add_parser("commit", help="Commit staged changes.")
    commit_parser.add_argument("message", help="Commit message.")

    # Command: log
    subparsers.add_parser("log", help="View commit history.")

    # Command: branch
    branch_parser = subparsers.add_parser("branch", help="Create a new branch.")
    branch_parser.add_argument("branch_name", help="Name of the branch.")

    # Command: checkout
    checkout_parser = subparsers.add_parser("checkout", help="Switch branches.")
    checkout_parser.add_argument("branch_name", help="Name of the branch to switch to.")

    # Command: merge
    merge_parser = subparsers.add_parser("merge", help="Merge a branch into the current branch.")
    merge_parser.add_argument("branch_name", help="Name of the branch to merge.")

    args = parser.parse_args()

    # Command execution
    if args.command == "init":
        init_repository()
    elif args.command == "add":
        add_file(args.file_path)
    elif args.command == "commit":
        commit(args.message)
    elif args.command == "log":
        log()
    elif args.command == "branch":
        create_branch(args.branch_name)
    elif args.command == "checkout":
        checkout_branch(args.branch_name)
    elif args.command == "merge":
        merge_branch(args.branch_name)
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
