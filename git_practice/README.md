# Giáo án Git

# Git Fetch

```bash
git fetch <remote_name> <branch_name>
```

# Git Pull

Pull all data from github to local. If a file is already in local, it will not be replaced

```bash
git pull <remote_name> <branch_name>
```

**NOTE**: If there are conflicts when `git pull` then git will ask to keep which files based on user, then we can use `git add` , `git commit` and then `git push` again

# Git Status

Check the history (Added, Modified, Deleted, Renamed, Copied, Updated but unmerged)

```bash
git status (-s)
```

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled.png)

# Git Show

Show files committed

```bash
git show (--commit_id) (--name-only)
```

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%201.png)

# Git Log

List all the times the user committed

```bash
git log (--graph) (--oneline) (--all)
```

The user has committed ‘first’ and ‘second’

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%202.png)

# Git Reset

Reset current HEAD to the specified commit

## Reset Soft

Reset commit but does not replace the local

```bash
git reset --soft <commit>
```

`commit` can be `HEAD~`, `HEAD^`, `ORIG_HEAD` .

We have 3 commit showed by `gitlog` 

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%203.png)

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%204.png)

## Reset Hard

Reset commit but replace the local to the last commit from `git log`

```bash
git reset --hard <commit>
```

# Git Revert

Revert all files and folders to the specific commit in local, then we can use `git push` to push to github

```bash
git revert <commit>
```

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%205.png)

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%206.png)

# Git Branch

Push to branch

```bash
# Create branch
git checkout -b <branch_name>
# Push to branch
git push <repo_name> <branch_name>
```

# Git Merge

Merge all files and folders to master, then we can use `git push` to push to github

```bash
# Change to master
git checkout master
git merge <branch_name>
```

# Git Rebase

Concatenate the master and branch

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%207.png)

```bash
git rebase <branch_name>
```

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%208.png)

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%209.png)

# Git Stash

Git Stash saves the newest changes into a box, multiple boxes will be organized like stack (FILO)

```bash
git stash save "<description>"
```

List all the stack boxes

```bash
git stash list
```

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%2010.png)

Get the box <num>

```bash
git stash apply (stash@{<num>})
```

Show the changes in the box <num>

```bash
git stash show (stash@{<num>}) (-p)
```

![Untitled](Gia%CC%81o%20a%CC%81n%20Git%20940d1379488d49a59708579be08a3f05/Untitled%2011.png)

Just like `git stash apply` but delete the box in stack

```bash
git stash pop (stash@{<num>})
```

Push box into new branches

```bash
git stash branch <new_branch_name> (<stash@{<num>}>)
```

Clear all boxes from stack

```bash
git stash clear
```

Delete specific box

```bash
git stash drop (<stash@{<num>}>)
```