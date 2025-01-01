# Pesapal Distributed Source Control System

Pesapal Distributed Source Control System (`vcs.py`) is a lightweight, Python-based version control system. It offers essential version control features such as repository initialization, file staging, committing changes, viewing commit history, and more.

---

## Features

- **Repository Initialization:** Create a `.myvcs` directory for tracking files and commits.
- **File Staging:** Stage files for the next commit.
- **Unstage Files:** Remove files from the staging area.
- **Commit Changes:** Record changes with a timestamp and message.
- **View History:** Display the commit log in reverse chronological order.
- **Check Status:** View the repository’s current state, including staged, unstaged, and untracked files.
- **Branch Management:** Create, delete, and switch between branches.

---

## Installation

1. Clone the repository and navigate to the directory:
   ```bash
   $ git clone <repository-url>
   $ cd <repository-folder>
   ```
2. Ensure Python 3 is installed on your system.

---

## Usage

Run the script with Python:
```bash
$ python3 vcs.py <command> [<args>]
```

### Commands

#### 1. Initialize Repository
```bash
$ python3 vcs.py init
```
Initializes a new repository in the current directory by creating a `.myvcs` folder.

#### 2. Add File
```bash
$ python3 vcs.py add <file_path>
```
Stages a file for the next commit.

#### 3. Unstage File
```bash
$ python3 vcs.py unstage <file_path>
```
Removes a file from the staging area.

#### 4. Commit Changes
```bash
$ python3 vcs.py commit "<message>"
```
Creates a new commit with the staged changes and a descriptive message.

#### 5. View Commit Log
```bash
$ python3 vcs.py log
```
Displays the commit history in reverse chronological order.

#### 6. Check Status
```bash
$ python3 vcs.py status
```
Displays the repository’s current state, including:
- Staged files
- Modified files
- Untracked files

#### 7. Create a New Branch
```bash
$ python3 vcs.py branch <branch_name >
```
Creates a new branch with the specified name.

#### 8. Switch Branch
```bash
$ python3 vcs.py checkout <branch_name>
```
Switches to the specified branch. Ensures that there are no uncommitted changes before switching.

---

### Example Workflow

1. **Initialize the repository:**
   ```bash
   $ python3 vcs.py init
   ```
2. **Add a file to the staging area:**
   ```bash
   $ python3 vcs.py add example.txt
   ```
3. **Check the repository status:**
   ```bash
   $ python3 vcs.py status
   ```
4. **Commit the changes:**
   ```bash
   $ python3 vcs.py commit "Initial commit"
   ```
5. **Create a new branch:**
   ```bash
   $ python3 vcs.py branch new-feature
   ```
6. **Switch to the new branch:**
   ```bash
   $ python3 vcs.py checkout new-feature
   ```
7. **View the commit log:**
   ```bash
   $ python3 vcs.py log
   ```
8. **Unstage a file:**
   ```bash
   $ python3 vcs.py unstage example.txt
   ```

---

## Error Handling

- **Repository Not Initialized:** Commands like `add`, `commit`, and `log` will prompt the user to initialize a repository if one is missing.
- **Missing Arguments:** If required arguments are not provided, the script will display usage instructions for the relevant command.
- **Non-Existent Files:** Attempting to stage or unstage a file that does not exist will result in an error message.
- **Empty Commits:** Commits without staged changes will return a warning and prevent creating an empty commit.
- **Uncommitted Changes:** Attempting to switch branches with uncommitted changes will prompt the user to commit or stash changes first.
- **Branch Existence:** Switching to or creating a branch will handle scenarios where the branch already exists or does not exist gracefully.

---

## Testing

To verify the system’s functionality, consider the following steps:

1. Test the basic workflow:
   - Initialize a repository.
   - Add, unstage, and commit files.
   - Check the status and log.
   - Create and switch branches.
2. Test edge cases:
   - Missing arguments.
   - Non-existent files during staging and unstaging.
   - Attempting commits without staged changes.
   - Switching branches with uncommitted changes.
3. Validate error messages for all invalid inputs.

---

## Future Improvements

- **Merge and Conflict Resolution:** Provide tools for merging changes and resolving conflicts.
- **File Differences:** Display changes between versions of files.
- **Remote Repository Support:** Enable pushing and pulling changes from remote repositories.
- **Improved Performance:** Optimize file hashing and storage for large repositories.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it.

