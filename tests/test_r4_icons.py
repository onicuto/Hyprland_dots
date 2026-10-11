"""Requirement R4 Test Suite: Local assets (.icons) optimization.

Verifies:
- .icons/ directory contains only active themes:
  - MacOS-Tahoe-Cursor (cursor theme)
  - default (cursor theme pointer)
  - MacTahoe-grey (icon theme)
- Unused heavy themes are completely deleted:
  - Bibata-Modern-Ice
  - Infinity
  - MacTahoe-grey-dark
  - MacTahoe-grey-light
- Total size of .icons/ directory is reduced and optimized (< 100 MB).
- No broken / dangling symlinks in /home/onicuto/.icons.
"""

import os
import unittest
from pathlib import Path
from typing import List

from tests.test_helpers import (
    HOME_DIR,
    REPO_ROOT,
    get_dir_size_bytes,
)


class TestR4Icons(unittest.TestCase):
    """Verifies icon and cursor themes preservation, unused themes deletion, and symlinks health."""

    def test_active_themes_exist_and_intact(self):
        """Active themes MacOS-Tahoe-Cursor, default, and MacTahoe-grey must exist in .icons/."""
        icons_dir = REPO_ROOT / ".icons"
        self.assertTrue(icons_dir.is_dir(), f".icons directory missing at {icons_dir}")

        # 1. MacOS-Tahoe-Cursor
        tahoe_cursor = icons_dir / "MacOS-Tahoe-Cursor"
        self.assertTrue(
            tahoe_cursor.is_dir(),
            f"Active cursor theme missing: {tahoe_cursor}",
        )
        self.assertTrue(
            (tahoe_cursor / "cursors").is_dir(),
            f"Active cursor theme {tahoe_cursor} missing 'cursors' directory",
        )

        # 2. default theme pointer
        default_theme = icons_dir / "default"
        self.assertTrue(
            default_theme.is_dir(),
            f"Active default theme pointer missing: {default_theme}",
        )
        default_index = default_theme / "index.theme"
        self.assertTrue(
            default_index.is_file(),
            f"Default theme missing index.theme at {default_index}",
        )
        content = default_index.read_text(encoding="utf-8")
        self.assertIn(
            "Inherits=MacOS-Tahoe-Cursor",
            content,
            f"default/index.theme must inherit MacOS-Tahoe-Cursor. Content: {content}",
        )

        # 3. MacTahoe-grey
        tahoe_grey = icons_dir / "MacTahoe-grey"
        self.assertTrue(
            tahoe_grey.is_dir(),
            f"Active icon theme missing: {tahoe_grey}",
        )
        self.assertTrue(
            (tahoe_grey / "index.theme").is_file(),
            f"Active icon theme {tahoe_grey} missing index.theme",
        )

    def test_unused_heavy_themes_deleted(self):
        """Unused heavy themes Bibata-Modern-Ice, Infinity, MacTahoe-grey-dark, MacTahoe-grey-light must be deleted."""
        icons_dir = REPO_ROOT / ".icons"
        unused_themes = [
            "Bibata-Modern-Ice",
            "Infinity",
            "MacTahoe-grey-dark",
            "MacTahoe-grey-light",
        ]

        found_themes = []
        for theme_name in unused_themes:
            p = icons_dir / theme_name
            if p.exists():
                found_themes.append(theme_name)

        self.assertEqual(
            found_themes,
            [],
            f"Unused heavy themes still present in .icons/: {found_themes}. These must be deleted to optimize repository size.",
        )

    def test_icons_directory_optimized_size(self):
        """The .icons/ directory size must be under 100 MB after pruning unused themes."""
        icons_dir = REPO_ROOT / ".icons"
        self.assertTrue(icons_dir.is_dir(), f".icons directory missing at {icons_dir}")

        total_bytes = get_dir_size_bytes(icons_dir)
        total_mb = total_bytes / (1024 * 1024)
        max_allowed_mb = 100.0

        self.assertLess(
            total_mb,
            max_allowed_mb,
            f".icons directory size is {total_mb:.2f} MB ({total_bytes} bytes), "
            "exceeding the 100 MB optimization threshold. Prune unused themes.",
        )

    def test_home_icons_symlinks_not_broken(self):
        """All symlinks in /home/onicuto/.icons must be valid (no dangling symlinks)."""
        home_icons = HOME_DIR / ".icons"
        if not home_icons.exists():
            return  # If user directory does not exist, nothing to check

        broken_symlinks: List[str] = []
        for entry in home_icons.iterdir():
            if entry.is_symlink():
                # Check if symlink target exists
                target = entry.resolve()
                if not target.exists():
                    broken_symlinks.append(f"{entry.name} -> {os.readlink(entry)} (target does not exist)")

        self.assertEqual(
            broken_symlinks,
            [],
            f"Broken symlinks detected in {home_icons}:\n"
            + "\n".join(broken_symlinks),
        )


if __name__ == "__main__":
    unittest.main()
