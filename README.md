# 📘 Comp Sci 28 — Collaborative Code Repository

A shared workspace for all Computer Science 28 coursemates to upload, learn, and collaborate on code.

---

## 🎯 Purpose
- Share assignments, practice code, and projects
- Learn from each other  
- Improve collaboration skills  
- Maintain organized code

---

## 🏗 Repository Structure


Folder Rules  
- Use your GitHub username, nickname, or real name for your folder  
- Create subfolders for each language with the corresponding code inside
- Do not edit other people’s folders without permission

---

## 🚀 Getting Started

### For Windows

For your Github account (if you don't have one), create a new account by clicking sign up and **this is important** continue with your Google Account. After a series of steps (and confirmations), it should be done! Simple and easy. Ensure you first send your GitHub usernames to me, so that I can give you write permissions (you won't be able to contribute otherwise). 

For Git, first go to your start menu and type **Command Prompt** to open the windows terminal. From there, type out (or copy): 

 ```bash
   winget install Git.git
 ```
And press enter to install the latest version of Git (if you don't have it already)

### For Mac

I wasn't able to verify it, as I did with Windows, but for Mac users, visit the [Homebrew](https://brew.sh/) website and follow the instructions to install it into your system. From there, type out (or copy):

```bash
   brew install git
 ```
to get started with git.

### How to start working with Git

Since most of us already have Visual Studio Code installed, I'm going to use it as an example. You first want to open your VS Code, and go to the Source Control Tab (or you could press Ctrl + Shift + G). 

Click on Manage Workspace Trust (in blue) and click Trust (or Ctrl + Enter) to either open a folder or Clone a repository. 

From there, you can clone the repo by clicking "Clone repository", providing this URL (https://github.com/compsciprojects2028-cloud/COMP-SCI-Projects-2028.git) in the searchbar. Select where you want the cloned repository to be, and just like that, you've completed the first and arguably most important step!

In that cloned repository, create a folder for your username, subfolders for the languages and code you want to submit and then open up your windows **command prompt** or Mac **terminal** to type the following sequence of instructions:

```bash
   cd <Insert the full path to the cloned repository here>
 ```
```bash
   git add <file or folder name>
 ```
```bash
   git commit -m "Add my folder and files"
 ```
```bash
   git push origin main
 ```

Remember to wrap files/folders containing spaces in quotation marks in your git add commands (e.g git add "file name.txt" instead of git add file name.txt), as doing this prevents parsing errors, and DM Ambrose on Telegram for further enquiries.
