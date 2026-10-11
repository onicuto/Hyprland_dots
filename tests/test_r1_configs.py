"""Requirement R1 Test Suite: Configuration files audit and remediation.

Verifies:
- All fish scripts pass `fish -n` syntax validation without errors.
- Fish config PATH additions are deduplicated.
- Waybar config parses as strict JSON without trailing commas.
- Waybar CSS syntax is valid with all referenced @ variables properly defined.
- Hyprland configuration passes verification and has no broken wallpaper references.
- Neofetch / Fastfetch configurations contain no foreign macOS paths or duplicate copy files.
- Qt5/Qt6 icon themes are aligned with installed/active themes.
- README documentation contains no broken asset references.
- Zero secrets, tokens, or private keys exist across the repository.
"""

import json
import os
import re
import unittest
from pathlib import Path
from typing import List

from tests.test_helpers import (
    REPO_ROOT,
    run_command,
    scan_file_for_secrets,
)


class TestR1FishScripts(unittest.TestCase):
    """Verifies Fish shell scripts syntax and environment cleanliness."""

    def test_all_fish_scripts_syntax(self):
        """All .fish files must pass `fish -n` syntax verification."""
        fish_dir = REPO_ROOT / ".config" / "fish"
        self.assertTrue(fish_dir.is_dir(), f"Fish config directory missing: {fish_dir}")

        fish_files: List[Path] = list(fish_dir.rglob("*.fish"))
        self.assertGreater(len(fish_files), 0, "No .fish scripts found to validate")

        syntax_failures = []
        for script in fish_files:
            rel_path = script.relative_to(REPO_ROOT)
            proc = run_command(f"fish -n '{script}'")
            if proc.returncode != 0:
                syntax_failures.append(f"{rel_path}: {proc.stderr.strip() or proc.stdout.strip()}")

        self.assertEqual(
            len(syntax_failures),
            0,
            f"Fish script syntax errors detected ({len(syntax_failures)} failures):\n"
            + "\n".join(syntax_failures),
        )

    def test_fish_config_path_deduplication(self):
        """config.fish should not redundantly re-add ~/.local/bin if already in conf.d/local-bin.fish."""
        config_fish = REPO_ROOT / ".config" / "fish" / "config.fish"
        local_bin_fish = REPO_ROOT / ".config" / "fish" / "conf.d" / "local-bin.fish"

        if local_bin_fish.is_file() and config_fish.is_file():
            content = config_fish.read_text(encoding="utf-8")
            # If local-bin.fish already exports PATH with ~/.local/bin, config.fish shouldn't duplicate it
            redundant_path_line = re.search(
                r'set\s+-gx\s+PATH\s+["\']?.*?\.local/bin["\']?\s+\$PATH',
                content,
            )
            self.assertIsNone(
                redundant_path_line,
                "config.fish contains redundant PATH addition for ~/.local/bin which is handled by conf.d/local-bin.fish",
            )


class TestR1WaybarConfig(unittest.TestCase):
    """Verifies Waybar configuration JSON and stylesheet integrity."""

    def test_waybar_config_strict_json(self):
        """Waybar config must parse as strict standard JSON without trailing commas."""
        config_path = REPO_ROOT / ".config" / "waybar" / "config"
        self.assertTrue(config_path.is_file(), f"Waybar config not found at {config_path}")

        raw_content = config_path.read_text(encoding="utf-8")
        try:
            parsed = json.loads(raw_content)
        except json.decoder.JSONDecodeError as err:
            self.fail(
                f"Waybar config failed strict JSON parsing: {err.msg} "
                f"at line {err.lineno}, column {err.colno} (char {err.pos})"
            )

        self.assertIsInstance(parsed, dict, "Waybar config must parse to a JSON object/dict")
        # Ensure modules are configured
        has_modules = any(
            k in parsed for k in ("modules-left", "modules-center", "modules-right")
        )
        self.assertTrue(has_modules, "Waybar config must contain modules-left/center/right definitions")

    def test_waybar_css_no_undefined_at_variables(self):
        """Waybar style.css must not use undefined @variables like @transparent."""
        style_css = REPO_ROOT / ".config" / "waybar" / "style.css"
        colors_css = REPO_ROOT / ".config" / "waybar" / "colors.css"

        self.assertTrue(style_css.is_file(), f"Waybar style.css missing at {style_css}")

        style_content = style_css.read_text(encoding="utf-8")
        colors_content = colors_css.read_text(encoding="utf-8") if colors_css.is_file() else ""

        # Extract all @define-color names
        defined_colors = set(re.findall(r"@define-color\s+([A-Za-z0-9_-]+)", colors_content + style_content))

        # Extract all @variable references in property values
        used_variables = set(re.findall(r":\s*@([A-Za-z0-9_-]+)", style_content))

        undefined = [v for v in used_variables if v not in defined_colors]
        self.assertEqual(
            undefined,
            [],
            f"Waybar style.css references undefined @variables: {undefined}. "
            "Use standard CSS property values (e.g. 'transparent' without '@') or define them via @define-color.",
        )


class TestR1HyprlandConfig(unittest.TestCase):
    """Verifies Hyprland compositor configuration and wallpaper assets."""

    def test_hyprland_verify_config(self):
        """hyprland --verify-config must succeed without errors."""
        config_path = REPO_ROOT / ".config" / "hypr" / "hyprland.conf"
        self.assertTrue(config_path.is_file(), f"Hyprland config missing at {config_path}")

        proc = run_command(f"hyprland --verify-config -c '{config_path}'")
        self.assertEqual(
            proc.returncode,
            0,
            f"Hyprland config verification failed with code {proc.returncode}:\n{proc.stderr}\n{proc.stdout}",
        )
        self.assertIn("config ok", proc.stdout.lower() + proc.stderr.lower(), "Expected 'config ok' in verification output")

    def test_hyprland_wallpaper_references_exist(self):
        """Wallpapers referenced in Hyprland configs must exist; deleted wallpapers must not be referenced."""
        hypr_dir = REPO_ROOT / ".config" / "hypr"
        self.assertTrue(hypr_dir.is_dir(), f"Hyprland directory missing at {hypr_dir}")

        # lubimaya.jpg was deleted; it must not be referenced anywhere in hyprland configs
        for conf_file in hypr_dir.rglob("*.conf"):
            content = conf_file.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn(
                "lubimaya.jpg",
                content,
                f"Deleted wallpaper 'lubimaya.jpg' still referenced in {conf_file.relative_to(REPO_ROOT)}",
            )

        # Check hyprlock.conf wallpaper reference
        hyprlock_conf = hypr_dir / "hyprlock.conf"
        if hyprlock_conf.is_file():
            content = hyprlock_conf.read_text(encoding="utf-8")
            path_matches = re.findall(r"path\s*=\s*([^\s#]+)", content)
            for path_str in path_matches:
                # Expand tilde or resolve relative path
                resolved_path = Path(os.path.expanduser(path_str))
                if not resolved_path.is_absolute():
                    resolved_path = (hypr_dir / path_str).resolve()
                self.assertTrue(
                    resolved_path.is_file(),
                    f"Wallpaper referenced in hyprlock.conf does not exist: {path_str} (resolved to {resolved_path})",
                )

    def test_hyprland_no_dead_neofetch_binary(self):
        """programs.conf must not reference non-existent /usr/bin/neofetch."""
        programs_conf = REPO_ROOT / ".config" / "hypr" / "programs.conf"
        if programs_conf.is_file():
            content = programs_conf.read_text(encoding="utf-8")
            self.assertNotIn(
                "/usr/bin/neofetch",
                content,
                "Dead reference to non-existent '/usr/bin/neofetch' found in programs.conf. Use fastfetch or remove.",
            )


class TestR1SystemFetchersAndDocumentation(unittest.TestCase):
    """Verifies fastfetch/neofetch paths, Qt theming, and documentation links."""

    def test_no_foreign_macos_paths_in_fetchers(self):
        """Configurations must not contain foreign macOS paths (/Users/haru)."""
        config_dir = REPO_ROOT / ".config"
        for conf_file in config_dir.rglob("*"):
            if conf_file.is_file() and conf_file.suffix in (".conf", ".jsonc", ".json"):
                content = conf_file.read_text(encoding="utf-8", errors="ignore")
                self.assertNotIn(
                    "/Users/haru",
                    content,
                    f"Foreign macOS path '/Users/haru' found in {conf_file.relative_to(REPO_ROOT)}",
                )

    def test_no_accidental_copy_config_files(self):
        """Accidental duplicate config files (e.g. 'config (copy 1).conf') must be eliminated."""
        suspicious = []
        for path in REPO_ROOT.rglob("*"):
            if any(part in path.parts for part in (".git", ".agents", "tests")):
                continue
            if path.is_file() and ("(copy" in path.name or path.name.endswith(".copy")):
                suspicious.append(path)
        self.assertEqual(
            suspicious,
            [],
            f"Found accidental duplicate config files with copy patterns in name: {suspicious}",
        )

    def test_qt_icon_theme_aligned(self):
        """qt5ct and qt6ct configs must reference existing/active theme MacTahoe-grey instead of missing Flat-Remix."""
        qt5_conf = REPO_ROOT / ".config" / "qt5ct" / "qt5ct.conf"
        qt6_conf = REPO_ROOT / ".config" / "qt6ct" / "qt6ct.conf"

        for conf in (qt5_conf, qt6_conf):
            if conf.is_file():
                content = conf.read_text(encoding="utf-8")
                self.assertNotIn(
                    "Flat-Remix-Blue",
                    content,
                    f"Missing theme 'Flat-Remix-Blue' configured in {conf.relative_to(REPO_ROOT)}. Align with 'MacTahoe-grey'.",
                )

    def test_readme_asset_links_valid(self):
        """README.md image references must point to existing assets."""
        readme = REPO_ROOT / "README.md"
        self.assertTrue(readme.is_file(), "README.md missing at repository root")

        content = readme.read_text(encoding="utf-8")
        image_refs = re.findall(r"!\[.*?\]\((.*?)\)", content)
        for ref in image_refs:
            if ref.startswith("http://") or ref.startswith("https://"):
                continue
            asset_path = (REPO_ROOT / ref).resolve()
            self.assertTrue(
                asset_path.is_file(),
                f"README.md references missing asset: '{ref}' (resolved to {asset_path})",
            )


class TestR1SecretScan(unittest.TestCase):
    """Verifies repository contains zero secrets, tokens, or private keys."""

    def test_zero_secrets_across_repository(self):
        """Scan all repository files to certify zero secrets or credentials exist."""
        violations = []
        ignored_dirs = {".git", ".agents", ".icons"}

        for root, dirs, files in os.walk(REPO_ROOT):
            # Modify dirs in-place to avoid descending into ignored directories
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for fname in files:
                # Do not scan test definitions themselves
                fpath = Path(root) / fname
                if "tests" in fpath.parts and fname.startswith("test_"):
                    continue

                findings = scan_file_for_secrets(fpath)
                for secret_type, line_no, preview in findings:
                    rel_p = fpath.relative_to(REPO_ROOT)
                    violations.append(
                        f"[{secret_type}] {rel_p}:{line_no} -> {preview[:30]}..."
                    )

        self.assertEqual(
            len(violations),
            0,
            f"Secret scan found {len(violations)} credentials in repo:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
