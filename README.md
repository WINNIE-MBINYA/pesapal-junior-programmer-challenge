# Pesapal Distributed Source Control System

Pesapal Distributed Source Control System (`pesapal_vcs.py`) is a lightweight version control system implemented in Python. It provides basic functionality to initialize a repository, add files, commit changes, and view commit history.

## Features

- **Repository Initialization:** Create a `.myvcs` directory for tracking files and commits.
- **File Staging:** Stage files for the next commit.
- **Commit Changes:** Record changes with a timestamp and message.
- **View History:** Display the commit log in reverse chronological order.

## Installation

Clone the repository and navigate to the directory:
```bash
$ git clone <repository-url>
$ cd <repository-folder>
```

Ensure Python 3 is installed on your system.

## Usage

Run the script with Python:
```bash
$ python pesapal_vcs.py <command> [<args>]
```

### Commands

#### 1. Initialize Repository
```bash
$ python pesapal_vcs.py init
```
Initializes a new repository in the current directory.

#### 2. Add File
```bash
$ python pesapal_vcs.py add <file_path>
```
Stages a file for the next commit.

#### 3. Commit Changes
```bash
$ python pesapal_vcs.py commit "<message>"
```
Creates a new commit with the staged changes.

#### 4. View Commit Log
```bash
$ python pesapal_vcs.py log
```
Displays the commit history.

### Example Workflow

1. Initialize the repository:
   ```bash
   $ python pesapal_vcs.py init
   ```

2. Add a file to the staging area:
   ```bash
   $ python pesapal_vcs.py add example.txt
   ```

3. Commit the changes:
   ```bash
   $ python pesapal_vcs.py commit "Initial commit"
   ```

4. View the commit log:
   ```bash
   $ python pesapal_vcs.py log
   ```

## Error Handling

- If a repository is not initialized, commands like `add`, `commit`, and `log` will prompt the user to initialize one.
- Missing arguments for commands will display usage instructions.
- Attempting to stage a non-existent file will return an error message.

## Testing

To ensure functionality:

1. Run various commands to test repository initialization, file staging, and commits.
2. Test with edge cases such as missing arguments, non-existent files, and empty commits.
3. Verify error handling for all invalid inputs.

## Future Improvements

- Add support for branches.
- Implement file differences.
- Add a remote repository system.

## License

This project is licensed under the MIT License.
