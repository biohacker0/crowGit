# crowGit
I built my own git, with two types : 1-with cli commands , 2-with prompts that lets you choose , it does git-add,commit,branch,change_branch,logs , we have flags with cli 

 mygit_cli.py is the one with cli commands, run it to use the cli version of my git:

- [blog:](#initialize-a-repository](https://corvus-ikshana.hashnode.dev/building-a-simple-gitcrowgit-like-version-control-system-in-python)
 

MyGit is a simplified version control system inspired by Git. It allows you to manage your project's version history, create branches, commit changes, and more, all from the command line.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Initialize a Repository](#initialize-a-repository)
  - [Add Files](#add-files)
  - [Commit Changes](#commit-changes)
  - [View Commit History](#view-commit-history)
  - [Create a Branch](#create-a-branch)
  - [Switch Branch](#switch-branch)
- [Contributing](#contributing)
- [License](#license)

#Installation
To use mygit_cli with cli commmands, follow these steps:

Clone the MyGit repository to your local machine:
1- git clone https://github.com/yourusername/mygit.git
2-cd mygit
3: have some files in the root folder to test it first , I have included some file in github already to test, I am working on it currently, so it not that stable.
#Commands
MyGit supports the following commands:

Sure, here's the text formatted in a more minimalist style for your GitHub README file:

---

## mygit_cli.py

This is a Python-based CLI for Git operations. Here are the available commands:

### init

Initialize a new Git repository in the current directory.

```bash
python mygit_cli.py init
```

### add

Add files to the Git index.

```bash
python mygit_cli.py add .
python mygit_cli.py add <filename>
```

`<filename>`: The name of the file you want to add to the index. Use `.` to add all files in the current directory and its subdirectories.

`--recursive, -r`: Recursively add files in the current directory and its subdirectories.

Examples:

```bash
python mygit_cli.py add .
python mygit_cli.py add myfile.txt
python mygit_cli.py add . --recursive
```

### commit

Commit changes to the Git repository.

```bash
python mygit_cli.py commit --message <message> --author <author> [--branch <branch>]
```

`--message`: The commit message.

`--author`: The name of the author.

`--branch`: (Optional) The branch name to commit to. If not specified, it will commit to the current branch.

Examples:

```bash
python mygit_cli.py commit --message "Initial commit" --author "John Doe"
python mygit_cli.py commit --message "Fix a bug" --author "Alice" --branch myfeaturebranch
```

### log

View commit history.

```bash
python mygit_cli.py log [--branch <branch>]
```

`--branch`: (Optional) The branch name to view commits. If not specified, it will show commits from the current branch

Examples:

```bash
python mygit_cli.py log
python mygit_cli.py log --branch myfeaturebranch
```

### create_branch

Create a new branch.

```bash
python mygit_cli.py create_branch <branch_name>
```

`<branch_name>`: The name of the new branch.

Example:

```bash
python mygit_cli.py create_branch myfeaturebranch
```

### switch_branch

Switch to an existing branch.

```bash
python mygit_cli.py switch_branch <branch_name>
```

`<branch_name>`: The name of the branch to switch to.

Example:

```bash
python mygit_cli.py switch_branch myfeaturebranch
```

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

To use the non cli version mygit.py , just run it and you will understand how to use it by using it, its simple, just choose a number like 1,2,3 etc , dont type the word init, choose the number associated with it.










