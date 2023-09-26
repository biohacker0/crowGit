# crowGit
I built my own git, with two types : 1-with cli commands , 2-with prompts that lets you choose , it does git-add,commit,branch,change_branch,logs , we have flags with cli 

# mygit_cli.py is the one with cli commands, run it to use the cli version of my git:
# MyGit - A Simple CLI Git-like Version Control System

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

#init
Initialize a new Git repository in the current directory.
` python mygit_cli.py init `
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  

#add
Add files to the Git index.
 ` python mygit_cli.py add . `
 ` python mygit_cli.py add <filename> `

<filename>: The name of the file you want to add to the index. Use . to add all files in the current directory and its subdirectories.
--recursive, -r: Recursively add files in the current directory and its subdirectories.

Examples:
python mygit_cli.py add .
python mygit_cli.py add myfile.txt
python mygit_cli.py add . --recursive

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#commit#
Commit changes to the Git repository.

` python mygit_cli.py commit --message <message> --author <author> [--branch <branch>] `
  
--message: The commit message.
--author: The name of the author.
--branch: (Optional) The branch name to commit to. If not specified, it will commit to the current branch.

Examples:

python mygit_cli.py commit --message "Initial commit" --author "John Doe"
python mygit_cli.py commit --message "Fix a bug" --author "Alice" --branch myfeaturebranch

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#log
View commit history.

` python mygit_cli.py log `

--branch: (Optional) The branch name to view commits. If not specified, it will show commits from the current branch

Examples:
python mygit_cli.py log
python mygit_cli.py log --branch myfeaturebranch

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#create_branch
Create a new branch.

` python mygit_cli.py create_branch <branch_name> `

<branch_name>: The name of the new branch.

Example:
python mygit_cli.py create_branch myfeaturebranch

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#switch_branch
Switch to an existing branch.

`python mygit_cli.py switch_branch <branch_name>`

<branch_name>: The name of the branch to switch to.

Example:
python mygit_cli.py switch_branch myfeaturebranch

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Usage
Here's a basic workflow using MyGit:

Initialize a new repository:
python mygit_cli.py init

Add files to the Git index:
python mygit_cli.py add myfile.txt

Or add all files in the current directory and its subdirectories:
python mygit_cli.py add . --recursive

Commit your changes:
python mygit_cli.py commit --message "Initial commit" --author "John Doe"

View the commit history:
python mygit_cli.py log

Create a new branch:
python mygit_cli.py create_branch myfeaturebranch

Switch to an existing branch:
python mygit_cli.py switch_branch myfeaturebranch










