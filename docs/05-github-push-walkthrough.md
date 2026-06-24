# GitHub Push Walkthrough

This creates a new, empty GitHub repository and pushes this kit into it. The same rules apply: one action per step, one path, a `Verify:` line after every step, no position words.

You need: the unzipped `crgs-lab-website-kit` folder, a GitHub account signed in, and Git installed on the computer doing the push.

---

## Part 1 · Create the empty repository

1. Go to `https://github.com/new`.
   - Verify: the "Create a new repository" form is shown.
2. Select the "Repository name" field.
   - Verify: a text cursor appears in the "Repository name" field.
3. Type `crgs-lab-website-kit`.
   - Verify: the field displays "crgs-lab-website-kit".
4. Select the "Private" option.
   - Verify: the "Private" option is marked.
5. Leave the "Add a README file" option unmarked.
   - Verify: the "Add a README file" option is not marked.
6. Leave the "Add .gitignore" option set to "None".
   - Verify: the ".gitignore" selector reads "None".
7. Select "Create repository".
   - Verify: GitHub shows a "Quick setup" page for an empty repository named `crgs-lab-website-kit`.

## Part 2 · Push the kit

Run each command in a terminal opened inside the unzipped `crgs-lab-website-kit` folder. Run one command per step.

1. Run: `cd crgs-lab-website-kit`
   - Verify: the terminal prompt now shows the `crgs-lab-website-kit` folder.
2. Run: `git init`
   - Verify: Git reports "Initialized empty Git repository".
3. Run: `git add .`
   - Verify: the command returns with no error.
4. Run: `git commit -m "CRGS Lab website build kit"`
   - Verify: Git reports the files were committed, listing a count of files changed.
5. Run: `git branch -M main`
   - Verify: the command returns with no error.
6. Run: `git remote add origin https://github.com/coreyalejandro/crgs-lab-website-kit.git`
   - Verify: the command returns with no error.
7. Run: `git push -u origin main`
   - Verify: Git reports the branch `main` was pushed and is tracking `origin/main`.

## Part 3 · Confirm

1. Reload the repository page at `https://github.com/coreyalejandro/crgs-lab-website-kit`.
   - Verify: the page now lists `README.md`, `mockup`, `assets`, `wordpress`, and `docs`.
2. Select the `mockup` folder.
   - Verify: the folder lists `index.html` and the `programs` folder.

**Push complete.** The kit lives in your new private repository, and nothing else was touched.

---

## If a command reports an error

- If step 2.4 reports an identity error, set it once with:
  - `git config --global user.email "you@example.com"`
  - `git config --global user.name "Corey Alejandro"`
  - Then run step 2.4 again.
- If step 2.7 reports an authentication error, GitHub now requires a Personal Access Token in place of a password. Create one at `https://github.com/settings/tokens`, then run step 2.7 again and paste the token when asked for a password.
