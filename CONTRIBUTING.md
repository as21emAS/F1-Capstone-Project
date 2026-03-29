# Contributing to F1 Race Predictor

This guide covers everything you need to know to contribute to this project as a team member. Read it before opening your first PR.

---

## Table of Contents

- [Branching Strategy](#branching-strategy)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)
- [Branch Protection Rules](#branch-protection-rules)

---

## Branching Strategy

We use an **increment-based branching strategy** aligned with our academic deliverable schedule.

```
main
└── increment-1          ← Increment 1 integration branch (due Feb 23)
    ├── feature/...      ← Individual work branches
    └── bugfix/...

└── increment-2          ← Increment 2 integration branch (due Mar 23)
    ├── feature/...
    └── bugfix/...

└── increment-3          ← Increment 3 integration branch (due Apr 27)
    ├── feature/...
    └── bugfix/...
```

### Branch Roles

| Branch | Purpose | Who merges into it |
|--------|----------|--------------------|
| `main` | Stable, professor-facing code. Only updated at the end of each increment. | PM (Alex) via PR from `increment-N` |
| `increment-N` | Integration branch for the current increment. All feature work targets this. | Any team member via PR |
| `feature/<name>` | Individual feature or task development | Author opens PR into `increment-N` |
| `bugfix/<description>` | Bug fix for a specific issue | Author opens PR into `increment-N` |

### Rules

- **Never push directly to `main`** — all changes go through a PR
- **Never push directly to `increment-N`** — all changes go through a PR from a feature branch
- Always branch off the **current `increment-N` branch**, not `main`
- Delete your feature branch after it's merged

---

## Branch Naming Conventions

```
feature/<your-initials>-<short-description>
bugfix/<your-initials>-<short-description>
```

Keep names lowercase, hyphen-separated, and descriptive.

**Good examples:**
```
feature/ah-health-endpoint
feature/bm-dashboard-layout
feature/ys-jolpica-api-client
bugfix/lr-migration-schema-mismatch
bugfix/js-model-prediction-null-check
```

**Bad examples:**
```
alex-branch          ← not descriptive
fix                  ← way too vague
Feature/Dashboard    ← don't use uppercase
my-work-stuff        ← not descriptive
```

---

## Commit Message Format

Follow the **Conventional Commits** standard. Every commit message must follow this format:

```
type(scope): brief description

- More detail if needed
- Reference issues: #123
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting, missing semicolons — no logic change |
| `refactor` | Code restructuring — no behavior change |
| `test` | Adding or updating tests |
| `chore` | Build process, dependency updates, config changes |
| `perf` | Performance improvements |

### Scopes

Use the component you're working in:

`dashboard` · `simulator` · `data-center` · `news` · `api` · `db` · `ml` · `auth` · `health` · `config` · `docs`

### Examples

```bash
feat(health): implement two-stage database health check endpoint

- Stage 1 checks DB connectivity with SELECT 1 and 3s timeout
- Stage 2 validates core table schema integrity
- Returns 503 with detailed status on failure
- Reference issues: #3

fix(db): resolve alembic migration path configuration

- Added prepend_sys_path to alembic.ini
- Fixed models import in env.py
- Reference issues: #7

docs(readme): update setup instructions for Jolpica-F1 API

chore(deps): update pydantic-settings to 2.x

refactor(api): extract health response builder into helper function
```

### Rules

- Use **present tense**: `add feature` not `added feature`
- Keep the first line **under 72 characters**
- Reference the GitHub issue number when applicable (`#123`)
- No period at the end of the subject line

---

## Pull Request Process

### Before Opening a PR

- [ ] Your branch is up to date with the target `increment-N` branch
- [ ] Your code runs locally without errors
- [ ] Backend: `uvicorn app.main:app --reload` starts cleanly
- [ ] Frontend: `npm run dev` starts cleanly
- [ ] No `.env` files or secrets committed
- [ ] No `node_modules/`, `venv/`, or build artifacts committed

### Opening a PR

1. Push your branch to GitHub:
   ```bash
   git push origin feature/ah-health-endpoint
   ```

2. Go to the repository on GitHub and click **"Compare & pull request"**

3. Set the **base branch** to the current `increment-N` branch (not `main`)

4. Fill out the PR template completely — don't delete sections, write N/A if not applicable

5. **Assign yourself** as the author

6. **Request a review** from at least one teammate

7. Link the related GitHub issue using `Closes #<issue-number>` in the PR description

### After Opening a PR

- Respond to review comments within **24 hours**
- Make requested changes on your branch and push — the PR updates automatically
- Do not merge your own PR — wait for reviewer approval
- Once approved, the reviewer or PM will merge

### Merge Strategy

We use **Squash and Merge** for all PRs into `increment-N`. This keeps the integration branch history clean. Your individual commits on the feature branch are squashed into a single commit with the PR title.

---

## Code Review Guidelines

### For Reviewers

**Turnaround:** Review PRs within **24 hours** of being assigned — blocked PRs block teammates.

**What to check:**
- Does the code do what the issue describes?
- Are there any obvious bugs or edge cases?
- Is the code readable and reasonably documented?
- Does it follow our naming conventions and structure?
- Are there any committed secrets, credentials, or build artifacts?

**How to give feedback:**
- Be specific — quote the line and explain the issue
- Distinguish between blocking issues and suggestions:
  - `[blocking]` — must be fixed before merge
  - `[suggestion]` — optional improvement, non-blocking
  - `[question]` — asking for clarification, non-blocking
- Approve when all blocking issues are resolved, even if suggestions remain

### For Authors

- Don't take feedback personally — reviews improve everyone's code
- If you disagree with feedback, explain your reasoning in a reply
- Mark threads as resolved after addressing them
- Don't push unrelated changes to an open PR

---

## Branch Protection Rules

The following rules are configured on GitHub for `main`. **These are enforced automatically.**

| Rule | Setting |
|------|---------|
| Require pull request before merging | ✅ Enabled |
| Required approvals | 1 |
| Dismiss stale reviews on new pushes | ✅ Enabled |
| Require status checks to pass | ✅ Enabled (when CI is set up) |
| Block direct pushes | ✅ Enabled |
| Allow force pushes | ❌ Disabled |

### Configuring Branch Protection (PM reference)

To set or update these rules on GitHub:

1. Go to the repository → **Settings** → **Branches**
2. Under **Branch protection rules**, click **Add rule** (or edit existing)
3. In **Branch name pattern**, enter `main`
4. Enable the rules listed above
5. Click **Save changes**

Repeat for `increment-N` branches as needed.