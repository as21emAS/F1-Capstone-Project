#!/usr/bin/env python3
"""
Create Increment 3 GitHub issues from increment3_issues_v3.yaml
Uses the GitHub CLI (gh) — must be authenticated before running.

Usage:
    python create_issues_inc3.py

Pre-flight:
    1. gh auth login  (if not already authenticated)
    2. Ensure the "Increment 3" milestone exists:
        print(f"    gh api repos/{REPO}/milestones --method POST --field title=\"{name}\" --field due_on=\"2026-04-27T23:59:59Z\"")
    3. Ensure all labels exist (script will warn if any are missing)
    4. Replace YOUR_HANDLE in the YAML with your actual GitHub username before running

The script checks for existing issues by title and skips duplicates.
"""

import subprocess
import sys
import yaml
import json
from pathlib import Path

REPO = "as21emAS/F1-Capstone-Project"
YAML_FILE = "increment3_issues_v3.yaml"

REQUIRED_LABELS = [
    "increment-3", "frontend", "backend", "ml", "data",
    "devops", "infra", "core", "buffer", "blocked"
]


def run(cmd: list[str], capture=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=capture, text=True)


def gh(*args, capture=True) -> subprocess.CompletedProcess:
    return run(["gh", *args], capture=capture)


def check_auth():
    result = gh("auth", "status")
    if result.returncode != 0:
        print("✗ Not authenticated. Run: gh auth login")
        sys.exit(1)
    print("✓ gh authenticated")


def check_milestone(name: str):
    result = gh("api", f"repos/{REPO}/milestones", "--jq", ".[].title")
    milestones = result.stdout.strip().splitlines()
    if name not in milestones:
        print(f"✗ Milestone '{name}' not found.")
        print(f"  Create it first:")
        print(f"    gh api repos/{REPO}/milestones --method POST --field title=\"{name}\" --field due_on=\"gi026-04-27T23:59:59Z\"")
        sys.exit(1)
    print(f"✓ Milestone '{name}' exists")


def check_labels():
    result = gh("api", f"repos/{REPO}/labels", "--jq", ".[].name")
    existing = set(result.stdout.strip().splitlines())
    missing = [l for l in REQUIRED_LABELS if l not in existing]
    if missing:
        print(f"⚠ Missing labels (will be created): {missing}")
        for label in missing:
            color = "E8002D" if label in ("increment-3", "core") else \
                    "0075ca" if label in ("frontend", "backend") else \
                    "e4e669" if label == "buffer" else \
                    "d93f0b" if label == "blocked" else "bfd4f2"
            gh("label", "create", label,
               "--color", color,
               "--repo", REPO)
            print(f"  Created label: {label}")
    else:
        print(f"✓ All labels exist")


def get_existing_titles() -> set[str]:
    result = gh("issue", "list",
                "--repo", REPO,
                "--state", "all",
                "--limit", "200",
                "--json", "title",
                "--jq", ".[].title")
    return set(result.stdout.strip().splitlines())



def create_issue(issue: dict, milestone_name: str, existing_titles: set[str]) -> bool:
    title = issue["title"]

    if title in existing_titles:
        print(f"  SKIP (exists): {title}")
        return False

    cmd = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", title,
        "--body", issue.get("body", ""),
    ]

    # Labels
    for label in issue.get("labels", []):
        cmd += ["--label", label]

    # Assignees — skip placeholder
    for assignee in issue.get("assignees", []):
        if assignee and "YOUR_HANDLE" not in assignee:
            cmd += ["--assignee", assignee]

    # Milestone
    cmd += ["--milestone", milestone_name]

    result = run(cmd)
    if result.returncode == 0:
        url = result.stdout.strip()
        print(f"  ✓ Created: {title}")
        print(f"    {url}")
        return True
    else:
        print(f"  ✗ Failed: {title}")
        print(f"    {result.stderr.strip()}")
        return False


def main():
    yaml_path = Path(YAML_FILE)
    if not yaml_path.exists():
        print(f"✗ YAML file not found: {YAML_FILE}")
        print(f"  Make sure you're running this from the same directory as the YAML.")
        sys.exit(1)

    with open(yaml_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    milestone_name = config["milestone"]
    issues = config["issues"]

    print(f"\n{'='*60}")
    print(f"  RaceWise → RACETRACK  |  Increment 3 Issue Creator")
    print(f"  Repo: {REPO}")
    print(f"  Issues to process: {len(issues)}")
    print(f"{'='*60}\n")

    # Pre-flight checks
    check_auth()
    check_milestone(milestone_name)
    check_labels()

    # Warn if any assignee is still YOUR_HANDLE
    placeholder_issues = [
        i["title"] for i in issues
        if "YOUR_HANDLE" in str(i.get("assignees", []))
    ]
    if placeholder_issues:
        print(f"\n⚠ YOUR_HANDLE placeholder found in {len(placeholder_issues)} issue(s).")
        print(f"  These will be created without an assignee. Fix in YAML to assign them:")
        for t in placeholder_issues:
            print(f"    - {t}")
        response = input("\n  Continue anyway? [y/N] ").strip().lower()
        if response != "y":
            print("Aborted. Update YOUR_HANDLE in the YAML and re-run.")
            sys.exit(0)

    # Fetch existing issues to deduplicate
    print(f"\nFetching existing issues...")
    existing_titles = get_existing_titles()
    print(f"Found {len(existing_titles)} existing issues")

    print(f"Milestone '{milestone_name}' found\n")

    # Create
    created = 0
    skipped = 0
    failed = 0

    core_issues = [i for i in issues if "buffer" not in i.get("labels", [])]
    buffer_issues = [i for i in issues if "buffer" in i.get("labels", [])]

    print(f"--- CORE ISSUES ({len(core_issues)}) ---")
    for issue in core_issues:
        result = create_issue(issue, milestone_name, existing_titles)
        if result is True:
            created += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1

    print(f"\n--- BUFFER ISSUES ({len(buffer_issues)}) ---")
    for issue in buffer_issues:
        result = create_issue(issue, milestone_name, existing_titles)
        if result is True:
            created += 1
        elif result is False:
            skipped += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"  Done.  Created: {created}  |  Skipped: {skipped}  |  Failed: {failed}")
    print(f"  View all: https://github.com/{REPO}/milestones")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
