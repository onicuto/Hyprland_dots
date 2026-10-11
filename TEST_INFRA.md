# Test Infrastructure & Specification: Dotfiles Acceptance Test Suite

## 1. Test Philosophy
This test infrastructure implements an **opaque-box, contract-driven, automated verification framework** for the system dotfiles repository (`/home/onicuto/.dotfiles`).

Core principles:
1. **Opaque-Box Verification**: The test suite observes only externally verifiable contracts, file contents, standard syntax tool exits (`fish -n`, `hyprland --verify-config`, `json.loads`), file-system attributes, Git database properties (`git fsck`, packfile/blob sizes), and absence of forbidden patterns (secrets, OS junk).
2. **Deterministic & Self-Contained**: The suite runs using standard Python 3.14+ library modules and native CLI utilities (`git`, `fish`, `hyprland`) with zero third-party pip dependencies, ensuring reliability across environments.
3. **Progressive Testability & Tiered Execution**: Tests are organized by requirement tier (`R1`, `R2`, `R3`, `R4`), allowing independent milestone validation while providing a unified E2E integration runner (`test_e2e.py` / `run_e2e_tests.sh`).
4. **Zero Tolerance Quality Gates**:
   - 0 syntax errors across shell, JSON, and CSS configurations.
   - 0 secrets, private keys, API tokens, or hardcoded passwords.
   - 0 untracked OS/editor/cache files.
   - 0 historical Git blobs exceeding 1.1 MB.
   - Strictly `< 50 MB` total `.git` directory size.
   - 0 broken symlinks and 0 unused heavy asset themes in `.icons`.

---

## 2. Feature Inventory & Requirement Mapping

| Req ID | Feature # | Component / Domain | Target Files | Verification Method & Assertions |
|---|---|---|---|---|
| **R1** | F1 | Fish Shell Syntax & Environment | `.config/fish/**/*.fish` | `fish -n <script>` exits 0; no redundant `PATH` re-export in `config.fish`. |
| **R1** | F2 | Waybar Configuration | `.config/waybar/config` | Strict `json.loads` parsing with 0 trailing commas; modules structure intact. |
| **R1** | F3 | Waybar Stylesheets | `.config/waybar/style.css`, `colors.css` | No undefined `@variable` references (e.g. `@transparent`); clean color definitions. |
| **R1** | F4 | Hyprland Compositor & Wallpapers | `.config/hypr/*.conf`, `scripts/wall` | `hyprland --verify-config` exits 0; all referenced wallpapers exist; deleted `lubimaya.jpg` unreferenced. |
| **R1** | F5 | Fetcher & Duplicate Configs | `.config/neofetch/`, `.config/fastfetch/` | No foreign macOS `/Users/` paths; accidental copy files (`config (copy 1).conf`) deleted. |
| **R1** | F6 | Qt Theming Alignment | `.config/qt5ct/`, `.config/qt6ct/` | `icon_theme` aligned to active `MacTahoe-grey` rather than missing `Flat-Remix-Blue-*`. |
| **R1** | F7 | Documentation Assets | `README.md` | All markdown image references (`assets/image.png`, etc.) resolve to existing files. |
| **R1** | F8 | Secret Scanning Certification | Repository-wide | Comprehensive regex scanning for RSA/EC/SSH keys, GitHub PATs, AWS, Slack, AI tokens. Found: 0. |
| **R2** | F9 | Production `.gitignore` Presence | `.gitignore` | Root `.gitignore` exists and contains non-trivial rules (> 50 chars). |
| **R2** | F10 | Comprehensive Pattern Coverage | `.gitignore` | `git check-ignore` validates rejection of `.agents/`, `.DS_Store`, `.swp`, `.bak`, caches, `.exe`, `.env`. |
| **R2** | F11 | Working Tree Cleanliness | Git Working Tree | `git status --porcelain` contains no untracked OS junk, backup files, or duplicate files. |
| **R3** | F12 | Local Backup Protection | Local filesystem & Git | Local backup ref/branch, clone mirror (`.dotfiles.backup.git`), or bundle (`.dotfiles_backup_all.bundle`) exists. |
| **R3** | F13 | Git History Blob Purge | Git Object Database | `git rev-list --objects --all` checked against size threshold; 0 blobs > 1.1 MB (1,153,433 bytes). |
| **R3** | F14 | Git Directory Size Constraint | `.git/` directory | Total recursive `.git/` size strictly `< 50 MB` (< 52,428,800 bytes). |
| **R3** | F15 | Git Integrity (`git fsck`) | Git Object Database | `git fsck --full --no-progress` exits 0 with 0 corruptions and 0 fatal errors. |
| **R4** | F16 | Active Themes Preservation | `.icons/` | `MacOS-Tahoe-Cursor`, `default` (`Inherits=MacOS-Tahoe-Cursor`), `MacTahoe-grey` intact with valid assets. |
| **R4** | F17 | Unused Heavy Themes Removal | `.icons/` | `Bibata-Modern-Ice`, `Infinity`, `MacTahoe-grey-dark`, `MacTahoe-grey-light` completely removed. |
| **R4** | F18 | Local Assets Size Optimization | `.icons/` | Total size of `.icons/` reduced to `< 100 MB` (saving ~104 MB and >30,000 files). |
| **R4** | F19 | User Symlink Integrity | `/home/onicuto/.icons` | 0 broken / dangling symlinks in user icons directory. |

---

## 3. Test Architecture & Directory Structure

```
/home/onicuto/.dotfiles/
├── TEST_INFRA.md               # Test infrastructure specification (this document)
├── TEST_READY.md               # Test readiness certification and execution guide
└── tests/
    ├── __init__.py             # Test package marker
    ├── test_helpers.py         # Shared helpers: paths, command runner, secret scanner, blob parser
    ├── test_r1_configs.py      # Requirement R1: Fish, Waybar, Hyprland, Qt, Readme, Secrets
    ├── test_r2_gitignore.py    # Requirement R2: Root .gitignore presence, coverage, tree cleanliness
    ├── test_r3_git_history.py  # Requirement R3: Backup existence, blob size <= 1.1MB, .git < 50MB, git fsck
    ├── test_r4_icons.py        # Requirement R4: Active themes, unused themes removal, size < 100MB, symlinks
    ├── test_e2e.py             # Unified CLI runner with formatted console & JSON outputs
    └── run_e2e_tests.sh        # Executable bash wrapper script
```

### Execution Flow
```
User / CI / Subagent Invocation
        │
        ▼
tests/run_e2e_tests.sh [ARGS]
        │
        ▼
tests/test_e2e.py [--tier {r1,r2,r3,r4,all}]
   ├── Tier R1: TestR1FishScripts, TestR1WaybarConfig, TestR1HyprlandConfig, ...
   ├── Tier R2: TestR2Gitignore
   ├── Tier R3: TestR3GitHistory
   └── Tier R4: TestR4Icons
        │
        ▼
Results Aggregator & Reporter
   ├── Console Formatted Output (ANSI colored table, defect breakdown)
   ├── JSON Output Mode (--json)
   └── Exit Code (0 on PASS, 1 on FAIL)
```

---

## 4. Coverage Thresholds & Quality Gates

| Metric | Target / Gate | Enforcement Test |
|---|---|---|
| **Fish Syntax Pass Rate** | 100% (0 errors) | `test_all_fish_scripts_syntax` |
| **Waybar JSON Standard Compliance** | Strict RFC 8259 (0 trailing commas) | `test_waybar_config_strict_json` |
| **Waybar CSS Variables** | 100% defined | `test_waybar_css_no_undefined_at_variables` |
| **Compositor Config Pass Rate** | 100% (exit code 0) | `test_hyprland_verify_config` |
| **Wallpaper Reference Validity** | 100% files present | `test_hyprland_wallpaper_references_exist` |
| **Repository Secret Occurrences** | Exactly 0 | `test_zero_secrets_across_repository` |
| **Root .gitignore Rule Count** | >= 7 tiers covered | `test_root_gitignore_exists_and_populated` |
| **Git Working Tree Untracked Junk** | 0 files | `test_git_status_clean_of_untracked_junk` |
| **Historical Git Blobs > 1.1 MB** | Exactly 0 | `test_no_large_blobs_in_git_history` |
| **.git Directory Total Size** | < 50 MB (52,428,800 bytes) | `test_git_directory_size_under_50mb` |
| **Git Object Database Health** | 100% clean (`git fsck` exit 0) | `test_git_fsck_full_passes` |
| **Unused Asset Themes in `.icons/`** | 0 present | `test_unused_heavy_themes_deleted` |
| **`.icons/` Total Disk Footprint** | < 100 MB | `test_icons_directory_optimized_size` |
| **Dangling Symlinks in `~/.icons`** | 0 broken symlinks | `test_home_icons_symlinks_not_broken` |
