# Git & Git CLI: End-to-End Interview Preparation Notes

---

## Table of Contents

1. [Fundamentals](#1-fundamentals)
2. [Basic Commands](#2-basic-commands)
3. [Branching & Merging](#3-branching--merging)
4. [Advanced Commands](#4-advanced-commands)
5. [Git Workflows & Strategies](#5-git-workflows--strategies)
6. [Git Internals & Object Model](#6-git-internals--object-model)
7. [Troubleshooting & Recovery](#7-troubleshooting--recovery)
8. [Practical Use Case Example](#8-practical-use-case-example)

---

## 1. Fundamentals

### What is Git?

Git is a **distributed version control system (DVCS)** that tracks changes in source code during software development. Created by Linus Torvalds in 2005, it enables:

- Tracking code changes over time
- Collaboration among multiple developers
- Reverting to previous versions
- Branching for parallel development
- Distributed architecture (every developer has a complete copy)

### Key Concepts

**Repository**: A file structure where Git stores all project files, metadata, and history. Can be local or remote.

**Commit**: A snapshot of the repository at a specific point in time with metadata (author, timestamp, message, parent commits).

**Branch**: An independent line of development. The default branch is typically `main` or `master`.

**HEAD**: A pointer to the current branch's last commit. Indicates which commit is checked out.

**Staging Area (Index)**: A buffer between your working directory and the repository. Contains files ready to be committed.

**Working Directory**: The actual files on your filesystem that you're editing.

**Remote Repository**: A Git repository hosted on a server (GitHub, GitLab, Bitbucket) used for collaboration.

### Git vs. Other VCS

| Aspect         | Git                            | SVN/Centralized VCS         |
| -------------- | ------------------------------ | --------------------------- |
| Architecture   | Distributed                    | Centralized                 |
| Offline Work   | Full functionality offline     | Limited without server      |
| Branching      | Fast and lightweight           | Expensive, full copies      |
| History        | Complete local history         | Server-dependent            |
| Performance    | Fast (local operations)        | Slower (network operations) |
| Merge Handling | Three-way merge, sophisticated | Basic merge algorithms      |

---

## 2. Basic Commands

### Initial Setup

```bash
# Check Git installation
git version

# Configure user information (required before committing)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# View all configuration
git config --list

# Configure for current repository only (omit --global)
git config user.name "Project-specific Name"
```

### Repository Creation & Cloning

```bash
# Initialize a new repository in current directory
git init

# Clone a remote repository
git clone <repository-url>

# Clone into a specific directory
git clone <repository-url> <directory-name>

# Clone with limited history (faster for large repos)
git clone --depth 1 <repository-url>
```

### Status & Information

```bash
# Show working directory status (modified, staged, untracked files)
git status

# Show detailed differences (unstaged changes)
git diff

# Show differences for staged changes
git diff --staged

# Show commit history
git log

# Show condensed log with one commit per line
git log --oneline

# Show log with graph visualization
git log --graph --oneline --all --decorate

# Show specific number of commits
git log -n 5

# Show commits with author and date
git log --pretty=format:"%h - %an - %ad - %s"

# Show changes in a specific commit
git show <commit-hash>

# Show file history (all commits affecting this file)
git log --follow -- <file-path>

# See who changed each line (blame)
git blame <file-path>
```

### Staging & Committing

```bash
# Add specific file to staging area
git add <file-path>

# Add all modified files
git add .

# Add all changes (tracked files only)
git add -A

# Interactive add (choose specific changes)
git add -p

# Remove file from staging area
git reset <file-path>

# Commit staged changes
git commit -m "Descriptive commit message"

# Commit with detailed message (opens editor)
git commit

# Commit all tracked files (skip staging area)
git commit -am "Message"

# Amend last commit (modify message or add files)
git commit --amend

# Amend without changing commit message
git commit --amend --no-edit
```

### Pushing & Pulling

```bash
# Push commits to remote branch
git push origin <branch-name>

# Push and set upstream branch (only first time)
git push -u origin <branch-name>

# Push all branches
git push origin --all

# Push specific commit
git push origin <commit-hash>:<branch-name>

# Fetch updates without merging
git fetch origin

# Fetch and merge (equivalent to fetch + merge)
git pull origin <branch-name>

# Pull with rebase instead of merge
git pull --rebase origin <branch-name>

# Delete remote branch
git push origin --delete <branch-name>

# Force push (use with caution)
git push origin <branch-name> --force
```

### Undoing Changes

```bash
# Discard changes to a file (revert to HEAD)
git checkout -- <file-path>

# Discard all changes in working directory
git checkout -- .

# Unstage a file
git reset <file-path>

# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset --mixed HEAD~1

# Undo last commit (discard all changes)
git reset --hard HEAD~1

# Undo last 3 commits
git reset --hard HEAD~3
```

---

## 3. Branching & Merging

### Branch Management

```bash
# List local branches
git branch

# List all branches (local and remote)
git branch -a

# List remote branches
git branch -r

# Create a new branch
git branch <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>

# Alternative: switch command (newer syntax)
git switch -c <branch-name>

# Switch to existing branch
git checkout <branch-name>

# Switch to previous branch
git checkout -

# Delete local branch
git branch -d <branch-name>

# Force delete branch
git branch -D <branch-name>

# Rename branch locally
git branch -m <old-name> <new-name>

# Set upstream for current branch
git branch -u origin/<branch-name>

# Show branch tracking information
git branch -vv
```

### Merging Strategies

```bash
# Basic merge (creates merge commit)
git merge <branch-name>

# Merge without creating merge commit (if possible)
git merge --ff-only <branch-name>

# Create merge commit even if fast-forward possible
git merge --no-ff <branch-name>

# Merge, resolve conflicts using "ours" strategy
git merge -s recursive -Xours <branch-name>

# Merge, resolve conflicts using "theirs" strategy
git merge -s recursive -Xtheirs <branch-name>

# Abort merge if conflicts arise
git merge --abort

# Continue merge after resolving conflicts
git add <resolved-files>
git commit
```

### Rebasing

```bash
# Rebase current branch onto another
git rebase <base-branch>

# Interactive rebase (allows editing, squashing, reordering commits)
git rebase -i HEAD~3  # Last 3 commits
git rebase -i <commit-hash>

# Continue rebase after resolving conflicts
git rebase --continue

# Skip current commit during rebase
git rebase --skip

# Abort rebase and return to original state
git rebase --abort

# Squash commits from feature branch before merging
git rebase -i main
# Change 'pick' to 'squash' for commits to combine
```

### Merge vs. Rebase

| Aspect        | Merge                       | Rebase                   |
| ------------- | --------------------------- | ------------------------ |
| History       | Creates merge commit        | Linear history           |
| Clarity       | Shows parallel development  | Clean timeline           |
| Collaboration | Safer for shared branches   | Best for local branches  |
| Conflicts     | Single merge conflict point | Multiple conflict points |
| Use Case      | Integration branches        | Feature branches         |

---

## 4. Advanced Commands

### Stashing

Temporarily save changes without committing them.

```bash
# Stash current changes
git stash

# Stash with descriptive message
git stash save "Work in progress on feature X"

# List all stashes
git stash list

# View specific stash contents
git stash show stash@{0}

# Show detailed diff of stash
git stash show -p stash@{0}

# Apply stash (keeps it in list)
git stash apply stash@{0}

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{n}

# Delete specific stash
git stash drop stash@{0}

# Delete all stashes
git stash clear

# Create branch from stash
git stash branch <branch-name> stash@{0}
```

### Cherry-Picking

Apply specific commits from one branch to another.

```bash
# Apply single commit to current branch
git cherry-pick <commit-hash>

# Apply multiple specific commits
git cherry-pick <commit1> <commit2> <commit3>

# Apply range of commits (exclusive start, inclusive end)
git cherry-pick <start-commit>..<end-commit>

# Continue cherry-pick after resolving conflicts
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort

# Skip current commit during cherry-pick
git cherry-pick --skip

# Cherry-pick without committing (allows editing)
git cherry-pick -n <commit-hash>
```

### Reset Explained

Three modes of git reset with different impacts:

```bash
# --soft: Move HEAD, keep changes staged
git reset --soft HEAD~1
# Use case: Undo commit but keep changes ready to re-commit

# --mixed (default): Move HEAD, unstage changes
git reset --mixed HEAD~1
# Use case: Undo commit and staging, but keep file changes

# --hard: Move HEAD, discard all changes
git reset --hard HEAD~1
# Use case: Completely discard commits and changes
```

**Comparison Table:**

| Mode    | HEAD    | Staging Area | Working Directory |
| ------- | ------- | ------------ | ----------------- |
| --soft  | Changed | Unchanged    | Unchanged         |
| --mixed | Changed | Changed      | Unchanged         |
| --hard  | Changed | Changed      | Changed           |

### Revert

Create new commits that undo previous commits (safer for shared branches).

```bash
# Create new commit that undoes a previous one
git revert <commit-hash>

# Revert without auto-committing (allows editing message)
git revert -n <commit-hash>

# Revert multiple commits
git revert <commit1>..<commit2>

# Continue or abort (similar to merge)
git revert --continue
git revert --abort
```

### Tags

Mark specific points in history (usually for releases).

```bash
# Create lightweight tag (simple reference)
git tag <tag-name>

# Create annotated tag (full metadata)
git tag -a <tag-name> -m "Version 1.0 release"

# List all tags
git tag

# Show tag information
git show <tag-name>

# Push specific tag
git push origin <tag-name>

# Push all tags
git push origin --tags

# Delete local tag
git tag -d <tag-name>

# Delete remote tag
git push origin --delete <tag-name>

# Checkout specific tag
git checkout <tag-name>
```

### Bisect

Find the commit that introduced a bug using binary search.

```bash
# Start bisect session
git bisect start

# Mark current commit as "bad" (has bug)
git bisect bad

# Mark a known good commit
git bisect good <commit-hash>

# Test current commit - mark as bad
git bisect bad

# Test current commit - mark as good
git bisect good

# End bisect session
git bisect reset

# Automatically bisect with script
git bisect run <test-script>
```

### Blame & Log Advanced

```bash
# Show line-by-line blame with commit info
git blame <file-path>

# Blame with email in output
git blame -e <file-path>

# Log filtering by author
git log --author="Name"

# Log filtering by date
git log --since="2 weeks ago"

# Log filtering by message
git log --grep="bug fix"

# Log specific to file changes
git log -- <file-path>

# Show all commits that modified specific line
git log -L<start>,<end>:<file-path>
```

---

## 5. Git Workflows & Strategies

### Git Flow

Complex workflow with multiple branch types. Best for versioned releases.

**Structure:**

- `main`: Production-ready code (tagged versions)
- `develop`: Integration branch for features
- `feature/*`: Feature branches (from develop)
- `release/*`: Release preparation branches (from develop)
- `hotfix/*`: Urgent fixes (from main)

**Workflow:**

```bash
# Feature development
git checkout -b feature/new-feature develop
# ... development ...
git checkout develop
git merge --no-ff feature/new-feature
git branch -d feature/new-feature

# Release preparation
git checkout -b release/1.0 develop
# ... version bumps, final testing ...
git checkout main
git merge --no-ff release/1.0 -m "Release 1.0"
git tag -a v1.0 -m "Version 1.0"
git checkout develop
git merge --no-ff release/1.0

# Hotfixes
git checkout -b hotfix/1.0.1 main
# ... apply fix ...
git checkout main
git merge --no-ff hotfix/1.0.1
git checkout develop
git merge --no-ff hotfix/1.0.1
```

**Pros:**

- Clear structure for multiple versions
- Well-defined stages
- Good for complex releases

**Cons:**

- Complex workflow
- Many branches to manage
- Not suitable for continuous delivery

### GitHub Flow

Simple, linear workflow. Best for continuous deployment.

**Rules:**

1. Main branch is always deployable
2. Create descriptive feature branches
3. Commit frequently with clear messages
4. Open pull requests for review
5. Merge after approval and tests pass
6. Delete branch after merge

**Workflow:**

```bash
# Create feature branch
git checkout -b feature/user-auth

# Make changes and commit
git commit -m "Add authentication logic"

# Push and create pull request
git push origin feature/user-auth

# After review and approval, merge via PR
# Delete branch
git branch -d feature/user-auth
```

**Pros:**

- Simple to understand
- Continuous delivery friendly
- Easy for small teams
- Rapid iteration

**Cons:**

- Not suited for multiple versions
- All code goes to production
- Less formal process

### Trunk-Based Development

All developers work on main with short-lived branches.

**Key Practices:**

- Short-lived branches (1-2 days max)
- Frequent integration to main
- Feature flags for incomplete features
- Automated testing required
- Continuous delivery focus

**Workflow:**

```bash
# Work on trunk with short branch
git checkout -b feature/quick-fix main

# Minimal development (few hours to day)
git commit -m "Quick improvement"

# Immediate merge after approval
git checkout main
git merge --squash feature/quick-fix
git branch -d feature/quick-fix
```

**Pros:**

- Reduces merge conflicts
- Facilitates continuous delivery
- Forces good testing practices
- Simple workflow

**Cons:**

- Requires mature CI/CD
- Challenging for large teams
- Feature flags complexity

### Branching Strategy Comparison

| Strategy    | Best For           | Complexity | Release Cycle |
| ----------- | ------------------ | ---------- | ------------- |
| Git Flow    | Versioned releases | High       | Scheduled     |
| GitHub Flow | Web applications   | Low        | Continuous    |
| Trunk-Based | DevOps teams       | Medium     | Real-time     |

---

## 6. Git Internals & Object Model

### Git Object Model

Git stores four types of objects:

**1. Blobs (Binary Large Objects)**

- Store file content
- Identified by SHA-1 hash of content
- No metadata (name, permissions stored in tree)
- Immutable

```
blob: [file content]
SHA-1: e69de29bb2d1d6434b8b29ae775ad8c2e48c5391
```

**2. Trees**

- Represent directory structures
- Contains references to blobs (files) and other trees (subdirectories)
- Store file names and permissions
- Identified by SHA-1 hash

```
tree:
  100644 blob abc123...  file.txt
  100755 blob def456...  script.sh
  040000 tree ghi789...  src/
```

**3. Commits**

- Snapshots of repository state
- Reference a tree object
- Store metadata: author, committer, timestamp, message
- Reference parent commit(s)
- Identified by SHA-1 hash

```
commit abc123:
  tree: def456
  parent: previous-commit-hash
  author: Name <email>
  date: timestamp
  message: "Commit message"
```

**4. Tags**

- Point to specific commits
- Two types: lightweight (reference) and annotated (full object)
- Used for marking releases or important points

```
tag v1.0:
  object: commit-hash
  type: commit
  tagger: Name <email>
  date: timestamp
  message: "Release 1.0"
```

### The .git Directory Structure

```
.git/
├── HEAD              # Current branch reference
├── config            # Repository configuration
├── description       # Repository description
├── index             # Staging area (binary)
├── objects/          # All Git objects (blobs, trees, commits, tags)
│   ├── ab/
│   ├── cd/
│   └── ...
├── refs/             # References to commits
│   ├── heads/        # Local branch pointers
│   ├── remotes/      # Remote tracking branches
│   └── tags/         # Tag references
├── logs/             # Reflog entries
├── hooks/            # Git hooks
└── info/
```

### How Git Identifies Objects

Every Git object is identified by **SHA-1 hash** of its contents:

```bash
# View object type and content
git cat-file -t <hash>        # Show type
git cat-file -p <hash>        # Show content
git cat-file -s <hash>        # Show size

# Example:
git cat-file -t abc123def  # Output: commit
git cat-file -p abc123def  # Output: commit details
```

### Commit Relationships

```
Commits form a directed acyclic graph (DAG):

Time →

o (HEAD, main) - Latest commit
|
o - Previous commit
|\
| o (feature branch)
|/
o - Common ancestor
|
o
|
o (initial commit)
```

---

## 7. Troubleshooting & Recovery

### Detached HEAD State

Occurs when HEAD points directly to a commit instead of a branch.

```bash
# How it happens:
git checkout abc123def          # Checkout specific commit
git checkout v1.0               # Checkout tag

# Check status
git status                       # Shows: HEAD detached at ...

# Fix - Create new branch from detached state:
git branch <new-branch>         # Create branch at current commit
git checkout -b <new-branch>    # Or create and switch in one command

# Or go back to branch:
git checkout main               # Return to main branch
```

### Merge Conflicts

When Git cannot automatically merge changes.

```bash
# Identify conflicted files:
git status

# View conflicts:
git diff                        # Show conflict details

# Conflict markers in file:
<<<<<<< HEAD
  your changes
=======
  incoming changes
>>>>>>> branch-name

# Resolution steps:
1. Edit file to keep desired code
2. Remove conflict markers
3. git add <file>
4. git commit
```

**Merge Conflict Resolution Strategies:**

```bash
# Abort merge if unsure:
git merge --abort

# Accept "ours" (current branch):
git checkout --ours <file>
git add <file>

# Accept "theirs" (incoming branch):
git checkout --theirs <file>
git add <file>

# Use merge tool:
git mergetool                   # Visual resolution
```

### Lost Commits & Reflog

**git reflog**: Reference log showing all HEAD movements.

```bash
# View reflog
git reflog                      # Show all HEAD changes
git reflog show origin/main     # Show specific branch reflog

# Reflog format:
abc123 HEAD@{0}: commit: Message
def456 HEAD@{1}: merge: Merged branch
ghi789 HEAD@{2}: checkout: moved to main

# Recover lost commit:
git checkout abc123             # Go to specific state
git branch recovery-branch      # Create branch from recovered commit

# Recover deleted branch:
git reflog                       # Find branch point
git checkout -b <branch> abc123 # Recreate from that point
```

### Common Errors & Solutions

**1. "fatal: The current branch main has no upstream branch"**

```bash
# Solution: Set upstream
git push -u origin main
git branch -u origin/main
```

**2. "refused to merge unrelated histories"**

```bash
# Solution: Allow unrelated histories
git merge --allow-unrelated-histories <branch>
```

**3. "fatal: not a git repository"**

```bash
# Solution: Initialize repository
git init
# Or navigate to git repository root
cd <git-repo>
```

**4. "Error: Your local changes would be overwritten by merge"**

```bash
# Solution: Stash changes or commit them
git stash                       # Temporary storage
git pull                        # Now safe to pull
```

**5. "Permission denied (publickey)"**

```bash
# Solution: Configure SSH keys
ssh-keygen -t rsa -b 4096
# Add public key to GitHub/GitLab
ssh -T git@github.com          # Test connection
```

### Performance Optimization for Large Repositories

```bash
# Garbage collection (cleanup and optimize)
git gc                          # Standard GC
git gc --aggressive             # More aggressive optimization

# Shallow clone (faster for large repos)
git clone --depth 1 <url>

# Clone with limited history
git clone --depth 100 <url>

# Sparse checkout (checkout only needed files)
git sparse-checkout init
git sparse-checkout set <directory>

# View repository size
du -sh .git

# List largest files in repository
git rev-list --all --objects | sort -k2 | tail -n 10
```

---

## 8. Practical Use Case Example

### Real-World Scenario: Team Banking Application Development

**Context:** A team of 4 developers building a banking application with ongoing feature development, bug fixes, and periodic releases.

**Branching Strategy:** GitHub Flow (simple, continuous deployment)

---

### Scenario 1: Feature Development with Code Review

**Developer A: Alice works on User Authentication**

```bash
# 1. Start fresh from main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-authentication

# 3. Develop and commit frequently
echo "// Login component" > login.js
git add login.js
git commit -m "Add login form component"

echo "// Authentication service" > auth-service.js
git add auth-service.js
git commit -m "Add authentication service with JWT support"

# 4. Push to remote (create PR)
git push -u origin feature/user-authentication

# 5. Code review feedback received: "Add password validation"
echo "// Validation logic" > validators.js
git add validators.js
git commit -m "Add password validation - addresses PR feedback"
git push origin feature/user-authentication

# 6. After approval, merge via GitHub PR interface
# Local cleanup:
git checkout main
git pull origin main
git branch -d feature/user-authentication
```

---

### Scenario 2: Concurrent Development with Merge Conflict

**Developer B: Bob working on Payment Processing**

```bash
# 1. Create feature branch
git checkout -b feature/payment-processing

# 2. Make changes to shared files
echo "// Payment service" > payment-service.js
git add payment-service.js
git commit -m "Add payment processing service"

# 3. While developing, main branch gets updated with auth feature
# Alice's authentication is merged to main

# 4. Update branch with latest main
git fetch origin
git rebase origin/main

# If conflict occurs during rebase:
# Edit conflicted files (both branches modified same lines)
# Then continue:
git add .
git rebase --continue

# 5. Push changes
git push origin feature/payment-processing
```

---

### Scenario 3: Bug Fix During Development (Context Switching)

**Developer C: Charlie finds a critical bug in production**

```bash
# 1. Save current work without committing
git stash save "WIP: implementing transaction rollback"

# 2. Create and switch to hotfix branch
git checkout -b bugfix/critical-payment-error main

# 3. Identify the problematic commit
git log --oneline | grep -i payment
# Output: abc1234 Add payment processing service

# 4. View changes in problematic commit
git show abc1234

# 5. Fix the bug
echo "// Fixed decimal precision issue" > payment-service.js
git add payment-service.js
git commit -m "Fix: Prevent payment amount precision loss in calculations"

# 6. Push and merge via PR
git push origin bugfix/critical-payment-error

# After merge approval:
git checkout main
git pull origin main

# 7. Merge same fix to other branches (if needed)
git checkout feature/payment-processing
git cherry-pick abc1234  # Apply the fix commit

# 8. Return to original work
git checkout feature/transaction-rollback  # Or branch name
git stash pop
```

---

### Scenario 4: Squashing Commits Before Merge

**Developer D: Diana finalizes a feature with multiple test commits**

```bash
# 1. Feature branch has many commits (including test commits)
git log --oneline feature/transaction-audit
# Output:
# xyz9999 Fix: Remove debug console logs
# xyz8888 Test: Add transaction audit tests
# xyz7777 Test: Add database tests
# xyz6666 Add transaction audit logging

# 2. Clean up history before merge using interactive rebase
git rebase -i main

# 3. In editor, mark commits to squash:
# pick xyz6666 Add transaction audit logging
# squash xyz7777 Test: Add database tests
# squash xyz8888 Test: Add transaction audit tests
# squash xyz9999 Fix: Remove debug console logs

# 4. Edit commit message in next editor window
# Consolidate messages into one meaningful message

# 5. Push (force push needed since history changed)
git push origin feature/transaction-audit --force-with-lease

# 6. Merge to main
git checkout main
git merge --no-ff feature/transaction-audit
```

---

### Scenario 5: Release Management

**Team Lead: Release preparation for v1.2**

```bash
# 1. Create release branch from develop (in this case, main)
git checkout -b release/v1.2 main

# 2. Update version numbers
echo "1.2.0" > VERSION
git add VERSION
git commit -m "Bump version to 1.2.0"

# 3. Minor fixes only on release branch
echo "// Production fix" > config.js
git add config.js
git commit -m "Fix: Configuration loading issue"

# 4. After testing, merge to main
git checkout main
git merge --no-ff release/v1.2
git tag -a v1.2.0 -m "Release version 1.2.0"

# 5. Update main with release changes
git push origin main --tags

# 6. Create release notes
git log --oneline v1.1.0..v1.2.0 > RELEASE_NOTES.md

# 7. Cleanup
git branch -d release/v1.2
```

---

### Scenario 6: Debugging with Bisect

**Finding which commit broke tests**

```bash
# 1. Start bisect session
git bisect start

# 2. Mark current as bad (tests fail)
git bisect bad

# 3. Mark known good commit (tests pass)
git bisect good v1.0

# Git automatically checks out commit halfway between

# 4. Run tests to determine if good or bad
npm test

# 5. If tests pass:
git bisect good

# If tests fail:
git bisect bad

# 6. Repeat until Git identifies the breaking commit
# Output: First bad commit: abc1234 (commit message)

# 7. Examine the problematic commit
git show abc1234
git bisect reset  # Exit bisect mode
```

---

### Scenario 7: Undoing Mistakes

**Various undo scenarios:**

```bash
# Case 1: Uncommitted changes - discard
git checkout -- payment-service.js

# Case 2: Staged changes - unstage
git reset payment-service.js

# Case 3: Wrong commit pushed - use revert (doesn't rewrite history)
git revert abc1234
git push origin main

# Case 4: Last 3 commits have issues - soft reset
git reset --soft HEAD~3
# Now make correct changes and re-commit

# Case 5: Accidentally deleted branch - recover with reflog
git reflog
git checkout -b restored-branch abc1234  # SHA from reflog
```

---

### Scenario 8: Collaboration Best Practices

**Daily workflow for team harmony:**

```bash
# Morning: Start with updated main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/new-endpoint

# During day: Frequent commits
git commit -m "Add user service"
git commit -m "Add endpoint validation"
git commit -m "Add error handling"

# End of day: Push changes for backup and visibility
git push -u origin feature/new-endpoint

# Keep updated with team changes
git fetch origin
git rebase origin/main        # Or merge if shared branch

# Before final merge: Ensure tests pass
npm test

# Create PR with clear description
git push origin feature/new-endpoint

# After approval and merge: Cleanup
git checkout main
git pull origin main
git branch -d feature/new-endpoint
```

---

## Command Reference Summary

### Most Used Commands

```bash
git init                        Initialize repository
git clone <url>                 Clone repository
git add <file>                  Stage changes
git commit -m "msg"             Commit changes
git push origin <branch>        Push to remote
git pull origin <branch>        Fetch and merge
git branch -b <name>            Create branch
git checkout <branch>           Switch branch
git merge <branch>              Merge branch
git log --oneline               View history
git status                       Check status
git diff                        View differences
```

### Recovery Commands

```bash
git stash                       Temporarily save changes
git reflog                      View HEAD history
git reset --soft HEAD~1         Undo commit (keep changes)
git revert <commit>             Create undo commit
git cherry-pick <commit>        Apply specific commit
git bisect                      Find breaking commit
```

### Collaboration Commands

```bash
git fetch                       Download remote changes
git rebase <branch>             Reapply commits
git merge --no-ff <branch>      Create merge commit
git branch -u origin/<branch>   Set upstream
git remote -v                   List remotes
```

---

## Interview Tips

1. **Explain the workflow**: Always describe your approach (feature branches, code review, testing)

2. **Know when to use what**: Merge for collaboration, rebase for clean history, reset for local cleanup

3. **Understand trade-offs**: Mention pros/cons of different strategies

4. **Have examples ready**: Prepare real scenarios you've handled (conflicts, recovery, etc.)

5. **Show Git internals knowledge**: Understand the object model and SHA-1 hashing

6. **Practice recovery**: Be comfortable with reflog, stash, and reset operations

7. **Know limitations**: Discuss why force push is dangerous and when it's necessary

8. **Stay current**: Mention new commands like `git switch` alongside older `git checkout`

---

## Additional Resources

- **Official Documentation**: `git help <command>` or https://git-scm.com
- **Interactive Learning**: GitHub Learning Lab
- **Visualization**: Use `git log --graph --all --oneline --decorate`
- **Configuration**: Review `.gitconfig` for optimization tips

---

_Last Updated: November 2025_
_Prepared for technical interviews with focus on practical scenarios and hands-on experience_
