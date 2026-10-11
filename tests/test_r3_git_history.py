"""Requirement R3 Test Suite: Git history rewrite, compression, and repository integrity.

Verifies:
- Local backup ref / clone / bundle exists before/after history rewrite.
- Git history contains 0 large blobs (> 1.1 MB).
- The .git directory size is strictly under 50 MB (< 52,428,800 bytes).
- `git fsck --full` exits 0 with zero errors or corruptions.
"""

import os
import unittest
from pathlib import Path
from typing import List

from tests.test_helpers import (
    HOME_DIR,
    REPO_ROOT,
    get_dir_size_bytes,
    get_git_objects_with_sizes,
    run_command,
)


class TestR3GitHistory(unittest.TestCase):
    """Verifies Git history purification, compression, and health."""

    def test_local_backup_exists(self):
        """A local backup ref, mirror clone, or bundle must exist."""
        # 1. Check local backup mirror directory
        mirror_path = HOME_DIR / ".dotfiles.backup.git"
        # 2. Check local git bundle
        bundle_path = HOME_DIR / ".dotfiles_backup_all.bundle"
        # 3. Check git branches / tags / refs for backup
        proc = run_command("git for-each-ref --format='%(refname)'")
        refs = proc.stdout.splitlines() if proc.returncode == 0 else []
        backup_refs = [r for r in refs if "backup" in r.lower()]

        has_backup = (
            mirror_path.is_dir()
            or bundle_path.is_file()
            or len(backup_refs) > 0
        )
        self.assertTrue(
            has_backup,
            "No local backup found! Expected at least one of:\n"
            f"1. Backup mirror at {mirror_path}\n"
            f"2. Backup bundle at {bundle_path}\n"
            f"3. Backup ref in git repository (e.g. refs/backup/* or refs/heads/backup)\n"
            f"Current refs: {refs}",
        )

    def test_no_large_blobs_in_git_history(self):
        """Git history must contain zero large blobs (> 1.1 MB / 1,153,433 bytes)."""
        # Threshold: 1.1 MB = 1.1 * 1024 * 1024 = 1,153,433 bytes
        max_bytes = int(1.1 * 1024 * 1024)

        all_objects = get_git_objects_with_sizes()
        large_blobs = [
            obj for obj in all_objects
            if obj["type"] == "blob" and obj["size"] > max_bytes
        ]

        if large_blobs:
            preview = [
                f"{b['sha'][:10]} ({b['size'] / (1024*1024):.2f} MB): {b['path']}"
                for b in large_blobs[:15]
            ]
            self.fail(
                f"Found {len(large_blobs)} blobs in git history exceeding 1.1 MB limit:\n"
                + "\n".join(preview)
                + (f"\n... and {len(large_blobs) - 15} more" if len(large_blobs) > 15 else "")
            )

    def test_git_directory_size_under_50mb(self):
        """The .git directory size must be strictly under 50 MB (52,428,800 bytes)."""
        git_dir = REPO_ROOT / ".git"
        self.assertTrue(git_dir.is_dir(), f".git directory not found at {git_dir}")

        total_bytes = get_dir_size_bytes(git_dir)
        total_mb = total_bytes / (1024 * 1024)
        max_allowed_mb = 50.0

        self.assertLess(
            total_mb,
            max_allowed_mb,
            f".git directory size is {total_mb:.2f} MB ({total_bytes} bytes), which exceeds the 50 MB threshold.",
        )

    def test_git_fsck_full_passes(self):
        """git fsck --full must complete cleanly with exit code 0 and no errors."""
        proc = run_command("git fsck --full --no-progress")
        self.assertEqual(
            proc.returncode,
            0,
            f"git fsck --full failed with exit code {proc.returncode}:\n{proc.stderr}\n{proc.stdout}",
        )
        self.assertNotIn("error:", proc.stderr.lower(), "git fsck reported errors in stderr")
        self.assertNotIn("fatal:", proc.stderr.lower(), "git fsck reported fatal errors in stderr")


if __name__ == "__main__":
    unittest.main()
