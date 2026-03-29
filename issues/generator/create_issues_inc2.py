# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
GitHub Issues Creator - F1 Predictor Increment 2

Creates GitHub issues, labels, and milestone from f1_increment2_issues.yml.
Requires: PyYAML, GitHub CLI (gh) authenticated.

Usage:
    python create_increment2_issues.py <owner/repo>

Example:
    python create_increment2_issues.py alexhsieh/f1-predictor
"""

import sys
import subprocess
import time

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)


YAML_FILE = "increment_2_issues.yml"


def run(cmd, capture=True):
    result = subprocess.run(cmd, capture_output=capture, text=True)
    return result


def check_gh_cli():
    result = run(["gh", "--version"])
    if result.returncode != 0:
        print("Error: GitHub CLI (gh) not installed. Visit https://cli.github.com/")
        sys.exit(1)
    print("✓ GitHub CLI found")


def check_auth(repo):
    result = run(["gh", "auth", "status"])
    if result.returncode != 0:
        print("Error: Not authenticated. Run: gh auth login")
        sys.exit(1)
    print("✓ GitHub CLI authenticated")


def create_milestone(repo, milestone_data):
    name = milestone_data["name"]
    description = milestone_data.get("description", "")
    due_date = milestone_data.get("due_date", "")

    cmd = [
        "gh", "api",
        f"/repos/{repo}/milestones",
        "--method", "POST",
        "-f", f"title={name}",
        "-f", f"description={description}",
        "-f", f"due_on={due_date}T23:59:59Z",
    ]
    result = run(cmd)
    if result.returncode == 0:
        print(f"✓ Created milestone: {name}")
    else:
        if "already_exists" in result.stderr or "Unprocessable" in result.stderr:
            print(f"  Milestone '{name}' already exists — skipping")
        else:
            print(f"  Warning: Could not create milestone '{name}': {result.stderr.strip()}")


def create_label(repo, label):
    name = label["name"]
    color = label.get("color", "ededed")
    description = label.get("description", "")

    cmd = [
        "gh", "api",
        f"/repos/{repo}/labels",
        "--method", "POST",
        "-f", f"name={name}",
        "-f", f"color={color}",
        "-f", f"description={description}",
    ]
    result = run(cmd)
    if result.returncode == 0:
        print(f"  ✓ Label: {name}")
    else:
        if "already_exists" in result.stderr or "Unprocessable" in result.stderr:
            print(f"  → Label '{name}' exists — skipping")
        else:
            print(f"  ✗ Label '{name}' failed: {result.stderr.strip()}")


def create_issue(repo, issue):
    title = issue["title"]
    body = issue.get("body", "")
    labels = issue.get("labels", [])
    milestone = issue.get("milestone", "")

    cmd = [
        "gh", "issue", "create",
        "--repo", repo,
        "--title", title,
        "--body", body,
    ]

    if labels:
        for label in labels:
            cmd += ["--label", label]

    if milestone:
        cmd += ["--milestone", milestone]

    result = run(cmd)
    if result.returncode == 0:
        url = result.stdout.strip()
        print(f"  ✓ {title}")
        print(f"    {url}")
        return True
    else:
        print(f"  ✗ FAILED: {title}")
        print(f"    {result.stderr.strip()}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python create_increment2_issues.py <owner/repo>")
        print("Example: python create_increment2_issues.py alexhsieh/f1-predictor")
        sys.exit(1)

    repo = sys.argv[1]

    print(f"\n F1 Predictor — Increment 2 GitHub Issues Creator")
    print(f"Repository: {repo}")
    print("=" * 55)

    # Preflight checks
    check_gh_cli()
    check_auth(repo)

    # Load YAML
    try:
        with open(YAML_FILE, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"\nError: '{YAML_FILE}' not found. Make sure it's in the same directory.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"\nError parsing YAML: {e}")
        sys.exit(1)

    # Create milestone
    print(f"\nCreating milestone...")
    if "milestone" in data:
        create_milestone(repo, data["milestone"])

    # Create labels
    print(f"\nCreating labels...")
    for label in data.get("labels", []):
        create_label(repo, label)

    # Create issues
    issues = data.get("issues", [])
    print(f"\n��� Creating {len(issues)} issues...")
    print("-" * 55)

    success = 0
    failed = 0
    for i, issue in enumerate(issues, 1):
        print(f"\n[{i}/{len(issues)}]")
        if create_issue(repo, issue):
            success += 1
        else:
            failed += 1
        # Small delay to avoid hitting GitHub API rate limits
        time.sleep(0.5)

    print("\n" + "=" * 55)
    print(f"✅ Success: {success} issues created")
    if failed:
        print(f"❌ Failed:  {failed} issues")
    print(f"��� Total:   {len(issues)} issues")
    print(f"\n��� View issues: https://github.com/{repo}/issues")
    print("=" * 55)


if __name__ == "__main__":
    main()
