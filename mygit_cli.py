import os
import argparse
import hashlib

# Define the path to the git repository
REPO_PATH = "mygit"

class TreeEntry:
    def __init__(self, name, is_directory, hash):
        self.name = name
        self.mode = "40000" if is_directory else "100644"
        self.hash = hash

class Tree:
    def __init__(self):
        self.entries = {}

    def hash(self):
        data = []
        for name, entry in sorted(self.entries.items()):
            data.append(f"{entry.mode} {name}\0{entry.hash}")
        return hash_object("".join(data).encode(), "tree")

def hash_object(data, obj_type):
    header = f"{obj_type} {len(data)}\0"
    full_data = header.encode() + data
    sha1_hash = hashlib.sha1(full_data).hexdigest()
    with open(f"{REPO_PATH}/objects/{sha1_hash}", "wb") as f:
        f.write(full_data)
    return sha1_hash

def create_tree():
    tree = Tree()
    for root, dirs, files in os.walk(".", topdown=True):
        subtree = Tree()
        for dir_name in dirs:
            subtree.entries[dir_name] = TreeEntry(dir_name, True, "")
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_content = open(file_path, "rb").read()
            file_hash = hash_object(file_content, "blob")
            subtree.entries[file_name] = TreeEntry(file_name, False, file_hash)
        dir_name = os.path.relpath(root, start=".")
        if dir_name == ".":
            dir_name = ""
        tree.entries[dir_name] = TreeEntry(dir_name, True, subtree.hash())
    return tree.hash()

def get_head_commit(branch="master"):
    head_file_path = os.path.join(REPO_PATH, "refs", "heads", branch)
    if os.path.isfile(head_file_path):
        with open(head_file_path, "r") as ref_file:
            return ref_file.read().strip()
    return None

def commit(args):
    repo_path = args.repo_path  # Get the repository path from args
    tree_hash = create_tree()

    # Determine the current branch dynamically if not provided
    current_branch = args.branch
    if current_branch is None:
        current_branch = get_current_branch(repo_path)

    parent_commit = get_head_commit(current_branch)
    commit_data = f"tree {tree_hash}\nauthor {args.author}\ncommitter {args.author}\n\n{args.message}\n"
    if parent_commit:
        commit_data += f"parent {parent_commit}\n"
    commit_hash = hash_object(commit_data.encode(), "commit")
    
    # Update the branch reference to the new commit
    branch_ref_path = os.path.join(repo_path, "refs", "heads", current_branch)
    with open(branch_ref_path, "w") as ref_file:
        ref_file.write(commit_hash)
    
    print(f"Committed: {commit_hash[:7]} to branch {current_branch}")
    return current_branch

def get_current_branch(repo_path):
    head_file_path = os.path.join(repo_path, "HEAD")
    if os.path.isfile(head_file_path):
        with open(head_file_path, "r") as head_file:
            ref = head_file.read().strip()
            if ref.startswith("ref: refs/heads/"):
                return ref[len("ref: refs/heads/"):]
    
    return create_default_branch(repo_path)

def create_default_branch(repo_path):
    branch_name = "default"
    branch_ref_path = os.path.join(repo_path, "refs", "heads", branch_name)
    with open(branch_ref_path, "w") as ref_file:
        ref_file.write("")
    update_head_ref(repo_path, branch_name)
    return branch_name

def create_branch(args):
    branch_name = args.branch_name
    branch_ref_path = os.path.join(args.repo_path, "refs", "heads", branch_name)
    if os.path.isfile(branch_ref_path):
        print(f"Branch '{branch_name}' already exists.")
    else:
        with open(branch_ref_path, "w") as ref_file:
            ref_file.write("")
        print(f"Created branch '{branch_name}'.")
    
    # Automatically switch to the newly created branch
    switch_branch(args)

    return branch_name

def switch_branch(args):
    branch_name = args.branch_name
    current_branch = get_head_commit(args.repo_path)
    if not branch_exists(branch_name, args.repo_path):
        print(f"Branch '{branch_name}' does not exist. Would you like to create it? (y/n)")
        choice = input().strip()
        if choice.lower() == 'y':
            create_branch(args)
        else:
            print("Aborted branch switch.")
            return current_branch
    update_head_ref(args.repo_path, branch_name)
    return branch_name

def branch_exists(branch_name, repo_path):
    branch_ref_path = os.path.join(repo_path, "refs", "heads", branch_name)
    return os.path.isfile(branch_ref_path)

def log(args):
    repo_path = args.repo_path  # Get the repository path from args
    branch_name = args.branch

    if branch_name is None:
        branches = [branch for branch in os.listdir(os.path.join(repo_path, "refs", "heads")) if os.path.isfile(os.path.join(repo_path, "refs", "heads", branch))]
        if not branches:
            print("No branches found.")
            return
        print("Available branches:")
        for branch in branches:
            print(f"- {branch}")
        branch_choice = input("Enter the branch name to view commits (or 'default' for default): ").strip()
        branch_name = branch_choice if branch_choice else "default"

    if not branch_exists(branch_name, repo_path):
        print(f"Branch '{branch_name}' does not exist.")
        return
    with open(os.path.join(repo_path, "refs", "heads", branch_name), "r") as ref_file:
        latest_commit = ref_file.read().strip()
    commit = latest_commit
    while commit:
        commit_path = os.path.join(repo_path, "objects", commit)
        with open(commit_path, "r") as commit_file:
            commit_data = commit_file.read()
        print(f"Commit: {commit[:7]}")
        lines = commit_data.split("\n")
        for line in lines:
            if line.startswith("author "):
                print(line)
        print(commit_data)
        lines = commit_data.split("\n")
        parent_commit = None
        for line in lines:
            if line.startswith("parent: "):
                parent_commit = line.split(": ")[1]
                break
        if parent_commit:
            print(f"Parent: {parent_commit}\n")
            commit = parent_commit
        else:
            break

def add(args):
    if args.filename == ".":
        # Adds all files in the current directory and subdirectories
        for root, dirs, files in os.walk(".", topdown=True):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                add_file(args.repo_path, file_path)
            if not args.recursive:
                break
    else:
        # Adds the specified file
        add_file(args.repo_path, args.filename)

def add_file(repo_path, file_path):
    file_content = open(file_path, "rb").read()
    file_hash = hash_object(file_content, "blob")
    index_path = os.path.join(repo_path, "index")
    with open(index_path, "a") as index_file:
        index_file.write(f"{file_hash} {file_path}\n")

def init(repo_path):
    os.makedirs(os.path.join(repo_path, "objects"))
    os.makedirs(os.path.join(repo_path, "refs", "heads"))
    create_default_branch(repo_path)
    tree_hash = create_tree()
    commit_data = f"tree {tree_hash}\nauthor Anonymous\ncommitter Anonymous\n\nInitial commit\n"
    initial_commit_hash = hash_object(commit_data.encode(), "commit")
    update_head_ref(repo_path, "default", initial_commit_hash)
    print("Initialized empty MyGit repository with an initial commit.")

def update_head_ref(repo_path, branch_name, commit_hash=None):
    head_ref_path = os.path.join(repo_path, "HEAD")
    if commit_hash is not None:
        with open(head_ref_path, "w") as head_file:
            head_file.write(f"ref: refs/heads/{branch_name}\n")
        branch_ref_path = os.path.join(repo_path, "refs", "heads", branch_name)
        with open(branch_ref_path, "w") as branch_file:
            branch_file.write(commit_hash)
    else:
        with open(head_ref_path, "w") as head_file:
            head_file.write(f"ref: refs/heads/{branch_name}\n")

def main():
    parser = argparse.ArgumentParser(description="MyGit - A simple Git-like version control system")
    parser.add_argument('--repo-path', default=REPO_PATH, help='Path to the Git repository')
    subparsers = parser.add_subparsers(dest="command", help='Subcommands')

    # init subcommand
    parser_init = subparsers.add_parser('init', help='Initialize a new Git repository')

    # add subcommand
    parser_add = subparsers.add_parser('add', help='Add files to the Git index')
    parser_add.add_argument('filename', help='Filename or "." to add all files')
    parser_add.add_argument('--recursive', '-r', action='store_true', help='Recursively add files')

    # commit subcommand
    parser_commit = subparsers.add_parser('commit', help='Commit changes to the Git repository')
    parser_commit.add_argument('--branch', help='Branch name to commit to (default is current branch)')
    parser_commit.add_argument('--message', required=True, help='Commit message')
    parser_commit.add_argument('--author', required=True, help="Author's name")

    # log subcommand
    parser_log = subparsers.add_parser('log', help='View commit history')
    parser_log.add_argument('--branch', help='Branch name to view commits (default is current branch)')

    # create branch subcommand
    parser_create_branch = subparsers.add_parser('create_branch', help='Create a new branch')
    parser_create_branch.add_argument('branch_name', help='Name of the new branch')

    # switch branch subcommand
    parser_switch_branch = subparsers.add_parser('switch_branch', help='Switch to an existing branch')
    parser_switch_branch.add_argument('branch_name', help='Name of the branch to switch to')

    args = parser.parse_args()

    if args.command == 'init':
        init(args.repo_path)
    elif args.command == 'add':
        add(args)
    elif args.command == 'commit':
        commit(args)
    elif args.command == 'log':
        log(args)
    elif args.command == 'create_branch':
        create_branch(args)
    elif args.command == 'switch_branch':
        switch_branch(args)
    else:
        print("Invalid command. Please choose a valid command.")

if __name__ == "__main__":
    main()
