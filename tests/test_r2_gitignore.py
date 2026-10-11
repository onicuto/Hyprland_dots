"""Requirement R2 Test Suite: .gitignore and untracked junk prevention.

Verifies:
- Production root .gitignore is present at /home/onicuto/.dotfiles/.gitignore.
- Gitignore covers 7 tiers:
  1. Multi-agent / runtime metadata (.agents/)
  2. OS metadata (.DS_Store, Thumbs.db)
  3. Editor / IDE temp files (*.swp, *.swo, *~, .vscode/, .idea/)
  4. Backup & scratch files (*.bak, *.tmp, *.old, *copy*)
  5. Application caches & native binaries (discord Cache, __pycache__, *.node)
  6. Binary installers / executables (*.exe, *.msi, *.so)
  7. Sensitive files & keys (*.env, *.key, *.pem, id_rsa)
- `git status` contains no untracked junk or temp files.
"""

import subprocess
import unittest
from pathlib import Path
from typing import List

from tests.test_helpers import (
    REPO_ROOT,
    run_command,
)


class TestR2Gitignore(unittest.TestCase):
    """Verifies presence, coverage, and efficacy of repository .gitignore."""

    def test_root_gitignore_exists_and_populated(self):
        """Root .gitignore file must exist and contain rules."""
        gitignore_path = REPO_ROOT / ".gitignore"
        self.assertTrue(
            gitignore_path.is_file(),
            f"Production .gitignore missing at {gitignore_path}",
        )
        content = gitignore_path.read_text(encoding="utf-8").strip()
        self.assertGreater(
            len(content),
            50,
            "Root .gitignore must contain non-trivial ignore rules",
        )

    def test_gitignore_covers_agent_artifacts(self):
        """Must ignore .agents/ runtime directory."""
        proc = run_command("git check-ignore -q .agents/some_file.md")
        self.assertEqual(
            proc.returncode,
            0,
            ".agents/ directory must be ignored by .gitignore",
        )

    def test_gitignore_covers_os_files(self):
        """Must ignore OS junk (.DS_Store, Thumbs.db)."""
        probe_paths = [
            ".DS_Store",
            ".config/fish/.DS_Store",
            "Thumbs.db",
        ]
        for probe in probe_paths:
            proc = run_command(f"git check-ignore -q '{probe}'")
            self.assertEqual(
                proc.returncode,
                0,
                f"OS artifact '{probe}' must be ignored by .gitignore",
            )

    def test_gitignore_covers_editor_and_backup_files(self):
        """Must ignore editor swap files, backup files, and IDE configs."""
        probe_paths = [
            "test.swp",
            "test.swo",
            "test.bak",
            ".config/fish/conf.d/fish_theme.fish.bak",
            "test.tmp",
            "test.old",
            ".vscode/settings.json",
            ".idea/workspace.xml",
        ]
        for probe in probe_paths:
            proc = run_command(f"git check-ignore -q '{probe}'")
            self.assertEqual(
                proc.returncode,
                0,
                f"Editor/backup pattern '{probe}' must be ignored by .gitignore",
            )

    def test_gitignore_covers_caches_and_binaries(self):
        """Must ignore app caches, electron HTTP caches, and executables."""
        probe_paths = [
            ".config/discord/Cache/Cache_Data/10437cc0e4254df4_0",
            ".config/discord/GPUCache/data_0",
            ".config/hydralauncher/CommonRedist/directx_Jun2010_redist.exe",
            "installer.msi",
            "test.node",
            "__pycache__/mod.pyc",
        ]
        for probe in probe_paths:
            proc = run_command(f"git check-ignore -q '{probe}'")
            self.assertEqual(
                proc.returncode,
                0,
                f"Cache/binary pattern '{probe}' must be ignored by .gitignore",
            )

    def test_gitignore_covers_sensitive_files(self):
        """Must ignore private keys, env files, and secrets."""
        probe_paths = [
            ".env",
            ".env.local",
            "id_rsa",
            "id_ed25519",
            "private.key",
            "server.pem",
        ]
        for probe in probe_paths:
            proc = run_command(f"git check-ignore -q '{probe}'")
            self.assertEqual(
                proc.returncode,
                0,
                f"Sensitive file pattern '{probe}' must be ignored by .gitignore",
            )

    def test_git_status_clean_of_untracked_junk(self):
        """git status must not contain untracked OS files, backups, or temp artifacts."""
        proc = run_command("git status --porcelain")
        self.assertEqual(proc.returncode, 0, "git status command failed")

        untracked_lines = [
            line[3:].strip()
            for line in proc.stdout.splitlines()
            if line.startswith("?? ")
        ]

        junk_extensions = {".DS_Store", ".bak", ".tmp", ".swp", ".swo", ".pyc", ".exe"}
        found_junk: List[str] = []
        for path_str in untracked_lines:
            p = Path(path_str)
            if p.name in (".DS_Store", "Thumbs.db") or p.suffix in junk_extensions:
                found_junk.append(path_str)
            if "(copy" in p.name:
                found_junk.append(path_str)

        self.assertEqual(
            found_junk,
            [],
            f"Untracked junk files detected in git working tree: {found_junk}",
        )


if __name__ == "__main__":
    unittest.main()
