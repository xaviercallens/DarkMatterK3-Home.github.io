#!/usr/bin/env python3
"""CI checker for TUNING_LOG.md discipline (EXECUTION_PLAN.md WP P0-D).

Rule: once PREDICTION.md carries a `PINNED:` header, any commit that edits
PREDICTION.md must edit TUNING_LOG.md in the same commit. Pre-pin edits are
exempt (no tuning event is possible before a value is frozen).

Usage:
    python3 scripts/check_tuning_log.py            # check history since last green run
    python3 scripts/check_tuning_log.py --selftest  # run the unit tests below, no git needed
"""
import subprocess
import sys


def commit_touches_file(commit_files: dict, sha: str, path: str) -> bool:
    return path in commit_files.get(sha, [])


def commit_pins_prediction(commit_prediction_text: dict, sha: str) -> bool:
    text = commit_prediction_text.get(sha, "")
    return "PINNED:" in text


def find_violations(commits: list, commit_files: dict, commit_prediction_text: dict) -> list:
    """commits: list of shas, oldest first.

    A violation is: PREDICTION.md was touched in `sha`, PREDICTION.md's content
    *at* `sha` already carries PINNED: (i.e. this is a post-pin edit, not the
    pinning commit itself), and TUNING_LOG.md was not touched in `sha`.
    """
    violations = []
    pinned_yet = False
    for sha in commits:
        touched_prediction = commit_touches_file(commit_files, sha, "PREDICTION.md")
        is_pinned_now = commit_pins_prediction(commit_prediction_text, sha)

        if touched_prediction and is_pinned_now and pinned_yet:
            if not commit_touches_file(commit_files, sha, "TUNING_LOG.md"):
                violations.append(sha)

        if is_pinned_now:
            pinned_yet = True

    return violations


def _git(args: list) -> str:
    return subprocess.run(
        ["git"] + args, capture_output=True, text=True, check=True
    ).stdout


def load_real_history() -> tuple:
    log = _git(["log", "--pretty=format:%H", "--reverse"]).splitlines()
    commit_files, commit_prediction_text = {}, {}
    for sha in log:
        files = _git(["show", "--name-only", "--pretty=format:", sha]).split()
        commit_files[sha] = files
        if "PREDICTION.md" in files:
            try:
                commit_prediction_text[sha] = _git(["show", f"{sha}:PREDICTION.md"])
            except subprocess.CalledProcessError:
                commit_prediction_text[sha] = ""  # file deleted in this commit
    return log, commit_files, commit_prediction_text


def run_selftest() -> int:
    # Golden-bad: post-pin edit to PREDICTION.md, no TUNING_LOG.md touch.
    commits = ["c0_draft", "c1_pin", "c2_bad_edit"]
    files = {
        "c0_draft": ["PREDICTION.md"],
        "c1_pin": ["PREDICTION.md"],
        "c2_bad_edit": ["PREDICTION.md"],  # missing TUNING_LOG.md
    }
    pred_text = {
        "c0_draft": "Status: draft",
        "c1_pin": "PINNED: abc123",
        "c2_bad_edit": "PINNED: abc123 (m_phi changed)",
    }
    violations = find_violations(commits, files, pred_text)
    assert violations == ["c2_bad_edit"], f"expected c2_bad_edit flagged, got {violations}"

    # Golden-good: same post-pin edit, but TUNING_LOG.md is touched too.
    files_good = dict(files)
    files_good["c2_bad_edit"] = ["PREDICTION.md", "TUNING_LOG.md"]
    violations_good = find_violations(commits, files_good, pred_text)
    assert violations_good == [], f"expected no violations, got {violations_good}"

    # Pre-pin edits never violate, even without TUNING_LOG.md.
    violations_pre = find_violations(["c0_draft"], files, pred_text)
    assert violations_pre == [], f"pre-pin edit incorrectly flagged: {violations_pre}"

    print("check_tuning_log.py self-test: PASS (3/3 control cases)")
    return 0


def run_check() -> int:
    commits, commit_files, commit_prediction_text = load_real_history()
    violations = find_violations(commits, commit_files, commit_prediction_text)
    if violations:
        print("BLOCKED by check_tuning_log: post-pin PREDICTION.md edit(s) with no "
              "matching TUNING_LOG.md entry in the same commit:")
        for sha in violations:
            print(f"  {sha}")
        print("Fix: add a TUNING_LOG.md row for each commit above (prereg-pipeline skill).")
        return 1
    print(f"check_tuning_log.py: OK ({len(commits)} commits checked, 0 violations)")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    sys.exit(run_check())
