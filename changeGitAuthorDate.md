# Changing Commit Authors / Dates

### Using Git Interactive Rebase:

1. Use `git rebase -i --root` or whichever commit you'd like to start with in place of `--root` such as `HEAD~3` which starts 3 commits before HEAD.
2. Underneath each commit `pick`, add the changes for that commit.
    - To change the commit author, add:  
        `exec git commit --amend --author="Author Name <email@address.com>" --no-edit`
    - To change the commit date, add:  
        `exec git commit --amend --date="Wed Jul 26 14:38:40 2023 -0500" --no-edit`  
        or  
        `exec GIT_AUTHOR_DATE="Wed Jul 26 14:38:40 2023 -0500" git commit --amend --no-edit`  
        or  
        `exec GIT_COMMITTER_DATE="Wed Jul 26 14:38:40 2023 -0500" git commit --amend --no-edit`
    - For easier copying:  
        ```
        exec git commit --amend --author="Author Name <email@address.com>" --no-edit
        exec GIT_AUTHOR_DATE="Wed Jul 26 14:38:40 2023 -0500" git commit --amend --no-edit
        exec GIT_COMMITTER_DATE="Wed Jul 26 14:38:40 2023 -0500" git commit --amend --no-edit
        ```
3. Save and close the interactive merge (On Vim, press `Esc`, type `:wq`, then hit `Enter`.).
4. Git will process those changes.  Finish with a `git push -f` to force the changes.


Something else that might help is changing the GitBash default editor.  Here is a table of possible options using the following link: https://koenwoortman.com/git-change-default-editor/

Changes the author name and email of commits from the last argument commit to current commit without changing dates.  Use `--root` to change all commits' authors, or `HEAD~4` to change last four commit authors, etc.:  
`git -c rebase.instructionFormat='%s%nexec GIT_COMMITTER_DATE="%cD" GIT_AUTHOR_DATE="%aD" git commit --amend --no-edit --author="Author <author@email.com>"' rebase -f --root`
