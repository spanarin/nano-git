
#!/usr/bin/env python3
import os
import hashlib
import json
import sys
import time

'''
Git - just files and folders in .git folder.

Data Structures

    blob = file contents

    index { file_path: blob_hash }

    commit { 
        hash: str,
        parent: parent_hash | None,
        tree: dict[file_path: str, blob_hash: str],
        message: str,
        timestamp: float
    }

'''
# ----- HELPERS ------ #
def hash_file(content: bytes) -> str:
    return hashlib.sha1(content).hexdigest()

# ----- COMMANDS ------ #
# creates .nanogit dir with empty objects (blob) dir, index and commits
def init():
    # empty blob (file contents) storage
    os.makedirs(".nanogit/objects", exist_ok=True)
    # empty staging storage
    with open(".nanogit/index.json", "w") as f:
        json.dump({}, f)
    # empty commits storage
    with open(".nanogit/commits.json", "w") as f:
        json.dump([], f)
    print("Initialized empty Nano Git repository.")

# cretes new blob object and updates index object
def add(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    h = hash_file(content)
    # store blob for file content
    with open(f".nanogit/objects/{h}", "wb") as f:
        f.write(content)
    # stage it
    index = json.load(open(".nanogit/index.json"))
    index[file_path] = h
    json.dump(index, open(".nanogit/index.json", "w"))

    print(f"Added {file_path} to staging with hash ({h[:7]}).") # notify user

# saves new commit object
def commit(message):
    index = json.load(open('.nanogit/index.json'))
    if not index:
        print("Please add files to staging.")
        return
    commits = json.load(open('.nanogit/commits.json'))
    parent = commits[-1]['hash'] if commits else None
    tree = index.copy()
    commit_hash = hash_file(json.dumps(tree).encode() + (parent.encode() if parent else b""))

    commit_obj = {
        "hash": commit_hash,
        "parent": parent,
        "tree": tree,
        "message": message,
        "timestamp": time.time()
    }
    commits.append(commit_obj)
    json.dump(commits, open('.nanogit/commits.json', "w"))
    # empty staging storage
    with open(".nanogit/index.json", "w") as f:
        json.dump({}, f)

    print(f"[{commit_hash[:7]}] {message}") # notify user

# prints all commits (new first)
def log():
    commits = json.load(open(".nanogit/commits.json"))
    for commit in reversed(commits): # reverse to see new ones first
        print(f"- commit [{commit['hash'][:7]}] {commit['message']}")

# restores files from blobs for specified commit
def checkout(commit_hash):
    commits = json.load(open(".nanogit/commits.json"))    
    commit = next((c for c in commits if c['hash'][:7] == commit_hash[:7]), None)
    if not commit:
        print(f"Commit [{commit_hash[:7]}] not found.")
        return   
    for path, blob_hash in commit['tree'].items():
        with open(path, "wb") as f:
            f.write(open(f".nanogit/objects/{blob_hash}","rb").read())

    print(f"Checked out commit [{commit_hash[:7]}].") # notify user


if __name__ == "__main__":
    print("nano-git@v1.0 - Git finally makes sense")

    if len(sys.argv) < 2:
        print('Usage: nano_git.py <command>')
    else:
        cmd = sys.argv[1]
        print(f"Executing command: {cmd}")
        if cmd == "init":
            init()
        elif cmd == "add":
            if len(sys.argv) >= 3:
                file_path = sys.argv[2]
                add(file_path)
            else:
                print('Usage: nano_git.py add <file_path>')
        elif cmd == "commit":
            if len(sys.argv) >= 3:
                message = sys.argv[2]
                commit(message)
            else:
                print('Usage: nano_git.py commit <message>')
        elif cmd == "log":
            log()
        elif cmd == "checkout":
            if len(sys.argv) >= 3:
                commit_hash = sys.argv[2]
                checkout(commit_hash)
            else:
                print('Usage: nano_git.py checkout <commit_hash>')
        else:
            print(f"Command '{cmd}' is not supported.")

