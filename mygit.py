import os
import hashlib

# Defines the path to the git repository
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

def commit(message, author="Anonymous", current_branch="master"):
    tree_hash = create_tree()
    parent_commit = get_head_commit(current_branch)
    commit_data = f"tree {tree_hash}\nauthor {author}\ncommitter {author}\n\n{message}\n"
    if parent_commit:
        commit_data += f"parent {parent_commit}\n"
    commit_hash = hash_object(commit_data.encode(), "commit")
    with open(os.path.join(REPO_PATH, "refs", "heads", current_branch), "w") as ref_file:
        ref_file.write(commit_hash)
    print(f"Committed: {commit_hash[:7]}")

def create_branch(branch_name):
    branch_ref_path = os.path.join(REPO_PATH, "refs", "heads", branch_name)
    if os.path.isfile(branch_ref_path):
        print(f"Branch '{branch_name}' already exists.")
    else:
        with open(branch_ref_path, "w") as ref_file:
            ref_file.write("")
        print(f"Created branch '{branch_name}'.")

def switch_branch(branch_name, current_branch):
    if not branch_exists(branch_name):
        print(f"Branch '{branch_name}' does not exist.")
        return current_branch
    return branch_name

def branch_exists(branch_name):
    branch_ref_path = os.path.join(REPO_PATH, "refs", "heads", branch_name)
    return os.path.isfile(branch_ref_path)

def log(current_branch="master"):
    branches = [branch for branch in os.listdir(os.path.join(REPO_PATH, "refs", "heads")) if os.path.isfile(os.path.join(REPO_PATH, "refs", "heads", branch))]
    if not branches:
        print("No branches found.")
        return
    print("Available branches:")
    for branch in branches:
        print(f"- {branch}")
    branch_choice = input("Enter the branch name to view commits (or 'master' for default): ").strip()
    current_branch = branch_choice if branch_choice else "master"
    if not branch_exists(current_branch):
        print(f"Branch '{current_branch}' does not exist.")
        return
    with open(os.path.join(REPO_PATH, "refs", "heads", current_branch), "r") as ref_file:
        latest_commit = ref_file.read().strip()
    commit = latest_commit
    while commit:
        commit_path = os.path.join(REPO_PATH, "objects", commit)
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

def add(filename, recursive=False):
    if filename == ".":
        # Adds all files in the current directory and subdirectories
        for root, dirs, files in os.walk(".", topdown=True):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                add_file(file_path)
            if not recursive:
                break
    else:
        # Adds the specified file
        add_file(filename)

def add_file(file_path):
    file_content = open(file_path, "rb").read()
    file_hash = hash_object(file_content, "blob")
    index_path = os.path.join(REPO_PATH, "index")
    with open(index_path, "a") as index_file:
        index_file.write(f"{file_hash} {file_path}\n")

def init():
    os.makedirs(os.path.join(REPO_PATH, "objects"))
    os.makedirs(os.path.join(REPO_PATH, "refs", "heads"))
    with open(os.path.join(REPO_PATH, "refs", "heads", "master"), "w") as ref_file:
        ref_file.write("")
    tree_hash = create_tree()
    commit_data = f"tree {tree_hash}\nauthor Anonymous\ncommitter Anonymous\n\nInitial commit\n"
    initial_commit_hash = hash_object(commit_data.encode(), "commit")
    with open(os.path.join(REPO_PATH, "refs", "heads", "master"), "w") as ref_file:
        ref_file.write(initial_commit_hash)
    print("Initialized empty MyGit repository with an initial commit.")

def main():
    print("Welcome to MyGit - a simple Git-like version control system.")
    current_branch = "master"  # Default branch

    while True:
        print("\nAvailable commands:")
        print("1. init - Initialize a new repository")
        print("2. add - Add files to the Git index")
        print("3. commit - Commit changes to the Git repository")
        print("4. log - View commit history")
        print("5. create branch - Create a new branch")
        print("6. switch branch - Switch to an existing branch")
        print("7. exit - Exit MyGit")

        choice = input("Enter a command number: ").strip()

        if choice == "1":
            init()
            print("Initialized empty MyGit repository.")
        elif choice == "2":
            filename = input("Enter the filename or '.' to add all files: ").strip()
            recursive = input("Recursive (y/n)? ").strip().lower() == "y"
            add(filename, recursive)
            print("Added files to the index.")
        elif choice == "3":
            branch_choice = input("Enter the branch name to commit to (or 'master' for default): ").strip()
            current_branch = branch_choice if branch_choice else "master"
            message = input("Enter a commit message: ").strip()
            author = input("Enter the author's name: ").strip()
            commit(message, author, current_branch)
        elif choice == "4":
            log(current_branch)
        elif choice == "5":
            branch_name = input("Enter branch name: ").strip()
            create_branch(branch_name)
        elif choice == "6":
            branch_name = input("Enter branch name to switch to: ").strip()
            current_branch = switch_branch(branch_name, current_branch)
        elif choice == "7":
            print("Exiting MyGit.")
            break
        else:
            print("Invalid command number. Please choose a valid command number.")

if __name__ == "__main__":
    main()
