# nano-git - Git finally makes sense

1-hour implementation of Git inner essentials in Python. Watch [YouTube video](https://youtu.be/p5CTL2s2Xno)

Mental model: 

> **Git** - just files and folders in `.git` folder.

## Usage:
```
python3 nano_git.py <command> <command_args>
```

Supported commads:
- init
- add
- commit
- log
- checkout

All commits hashes are shown as first 7 chars as in Git.

Not included for simplicity:
- branches (branch & checkout)
- merge
- diff
- rebase


## Workflow example

```bash
python3 nano_git.py init
python3 nano_git.py add file1.txt
python3 nano_git.py commit "added file1.txt"
python3 nano_git.py log
python3 nano_git.py add file2.txt
python3 nano_git.py commit "added file2.txt"
python3 nano_git.py log
python3 nano_git.py checkout <hash>
```

## Data structures

```
    blob = file contents

    index { file_path: blob_hash }

    commit { 
        hash: str,
        parent: parent_hash | None,
        tree: dict[file_path: str, blob_hash: str],
        message: str,
        timestamp: float
    }
```

## Tech stack

- hashlib (SHA-1 hashes)
- sys (args handling)
- os (file/dirs handling)
- json (git data structures handling)
- time (commits timestamps)
