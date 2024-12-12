# Pesapal Distributed Source Control System

import os
import hashlib
import pickle
from datetime import datetime
import shutil
import difflib

# Constants for the VCS system
VCS_DIR = ".myvcs"
INDEX_FILE = "index"
COMMITS_DIR = "commits"
REFS_DIR = "refs"
HEAD_FILE = "HEAD"

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

    print("Initialized empty repository in .myvcs")

def hash_file(file_path):
    """Calculates the hash of a file."""
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def add_file(file_path):
    """Stages a file for the next commit."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    file_hash = hash_file(file_path)
    with open(os.path.join(VCS_DIR, INDEX_FILE), 'rb') as index_file:
        index = pickle.load(index_file)

    index[file_path] = file_hash

    with open(os.path.join(VCS_DIR, INDEX_FILE), 'wb') as index_file:
        pickle.dump(index, index_file)

    print(f"Staged {file_path}")

def commit(message):
    """Creates a new commit."""
    if not os.path.exists(VCS_DIR):
        print("No repository found. Please initialize one.")
        return

    with open(os.path.join(VCS_DIR, INDEX_FILE), 'rb') as index_file:
        index = pickle.load(index_file)

    if not index:
        print("No changes to commit.")
        return

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
        "files": index.copy()
    }

    commit_hash = hashlib.sha1(pickle.dumps(commit_data)).hexdigest()
    commit_path = os.path.join(VCS_DIR, COMMITS_DIR, commit_hash)
    
    with open(commit_path, 'wb') as commit_file:
        pickle.dump(commit_data, commit_file)

    with open(branch_path, 'w') as branch_file:
        branch_file.write(commit_hash)

    with open(os.path.join(VCS_DIR, INDEX_FILE), 'wb') as index_file:
        pickle.dump({}, index_file)

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

# CLI
if __name__ == "__main__":
    import sys

    commands = {
        "init": init_repository,
        "add": add_file,
        "commit": commit,
        "log": log,
    }

    if len(sys.argv) < 2:
        print("Usage: vcs <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command in commands:
        try:
            # Check if the correct number of arguments is provided
            if command == "add" and len(sys.argv) < 3:
                print("Usage: vcs add <file_path>")
                sys.exit(1)
            elif command == "commit" and len(sys.argv) < 3:
                print("Usage: vcs commit <message>")
                sys.exit(1)

            commands[command](*sys.argv[2:])
        except TypeError:
            print(f"Invalid arguments for command: {command}")
            print("Usage: vcs <command> [<args>]")
    else:
        print(f"Unknown command: {command}")
