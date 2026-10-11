# Project: Dotfiles Comprehensive Audit and Optimization

## Architecture
This project audits, fixes, cleans, and optimizes the user's system dotfiles repository (`/home/onicuto/.dotfiles`).
The repository contains Wayland/Hyprland desktop configuration, status bar (Waybar), shell (fish), editor (nvim), terminal (ghostty), desktop assets (`.icons`), and Git history.

Data Flow and Integration:
1. Compositor & GUI: Hyprland (`.config/hypr/`) coordinates window management, wallpaper display, cursor settings (`MacOS-Tahoe-Cursor`), and launches Waybar, Ghostty, Wofi, Cava.
2. Theming & Assets: GTK (`.config/gtk-3.0/`, `.config/gtk-4.0/`) and Qt (`.config/qt5ct/`, `.config/qt6ct/`) configure `MacTahoe-grey` icon theme and `MacOS-Tahoe-Cursor` cursor theme from `.icons/`.
3. Shell & CLI: Fish (`.config/fish/`) configures path, prompt, and interactive aliases.
4. Git Repository & History: Tracks dotfiles with `.gitignore` protection; historical commits purged of 128 large non-dotfiles blobs (>1 MB) to compress `.git` to <50 MB with 100% clean `git fsck`.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Fish Syntax & PATH Verification | Verify `fish -n` syntax on all `.fish` files, eliminate duplicate PATH additions in `config.fish` | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Waybar JSON Trailing Commas | Eliminate trailing commas in `.config/waybar/config` (lines 106, 160) for strict standard JSON validity | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Waybar CSS Styling Fixes | Fix `@transparent` reference in `style.css` and deduplicate `@define-color` definitions in `colors.css` | M1 | ORIGINAL_REQUEST §R1 |
| 4 | Hyprland Config & Wallpaper Validation | Remove dead `/usr/bin/neofetch` reference in `programs.conf`, ensure staged deletion of `lubimaya.jpg`, verify wallpaper references | M1 | ORIGINAL_REQUEST §R1 |
| 5 | Neofetch / Fastfetch Path Remediation | Fix foreign `/Users/haru` macOS path in `neofetch/config.jsonc`, delete accidental duplicate `config (copy 1).conf` | M1 | ORIGINAL_REQUEST §R1 |
| 6 | Qt Icon Theme Alignment | Align `qt5ct.conf` and `qt6ct.conf` icon theme from missing `Flat-Remix-Blue-*` to active `MacTahoe-grey` | M1 | ORIGINAL_REQUEST §R1 |
| 7 | README Documentation Fixes | Fix broken reference to missing `assets/image.png` and convert absolute hardcoded paths to relative links | M1 | ORIGINAL_REQUEST §R1 |
| 8 | Secret Scanning Certification | Ensure zero private keys, API keys, credentials, or tokens exist across all repository files | M1 | ORIGINAL_REQUEST §R1 |
| 9 | Comprehensive .gitignore | Create production 7-tier `.gitignore` covering `.agents/`, OS files, editor temps, caches, binaries, and secrets | M2 | ORIGINAL_REQUEST §R2 |
| 10 | Git Index Junk Purge | Remove tracked `.DS_Store` files, `.bak` backup file, and duplicate configs from Git index | M2 | ORIGINAL_REQUEST §R2 |
| 11 | .icons Theme Audit & Optimization | Remove unreferenced heavy themes (`Bibata-Modern-Ice`, `Infinity`, `MacTahoe-grey-dark`, `MacTahoe-grey-light`) | M3 | ORIGINAL_REQUEST §R4 |
| 12 | Preserve Active Cursor & Icon Themes | Retain `MacOS-Tahoe-Cursor`, `default`, and `MacTahoe-grey` intact in `.icons/` | M3 | ORIGINAL_REQUEST §R4 |
| 13 | Local Symlink Cleanup | Clean up dangling symlinks in `/home/onicuto/.icons` pointing to removed themes | M3 | ORIGINAL_REQUEST §R4 |
| 14 | Local Git Backup Ref & Mirror | Create full backup mirror `/home/onicuto/.dotfiles.backup.git` and bundle `/home/onicuto/.dotfiles_backup_all.bundle` before rewrite | M4 | ORIGINAL_REQUEST §R3 |
| 15 | Purge Historical Blobs > 1 MB | Use `git-filter-repo` to strip non-config large blobs (>1100KB) and purge historical non-dotfiles application directories | M4 | ORIGINAL_REQUEST §R3 |
| 16 | Git Reflog Expire & Aggressive Repack | Run `git reflog expire --expire=now --all` and `git gc --prune=now --aggressive` to reduce `.git` < 50 MB | M4 | ORIGINAL_REQUEST §R3 |
| 17 | Git Integrity & Remote Re-establishment | Verify `git fsck --full` passes cleanly with zero errors; re-link remote origin | M4 | ORIGINAL_REQUEST §R3 |
| 18 | E2E Full Acceptance Criteria & Forensic Audit | Validate all acceptance criteria across R1-R4 with independent checks and forensic integrity verification | M5 | ORIGINAL_REQUEST §Acceptance Criteria |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Config Audit & Remediation | Fix Waybar JSON/CSS, Hyprland dead refs/wallpaper, Neofetch paths, Qt themes, README, verify fish syntax & 0 secrets | none | DONE |
| M2 | Gitignore & Junk Prevention | Create comprehensive `.gitignore`, purge tracked `.DS_Store`, `.bak`, and duplicate configs | M1 | DONE |
| M3 | Local Assets (.icons) Optimization | Delete 4 unused heavy themes (save 104 MB / 30,882 files), retain active cursor/icon themes, clean dangling symlinks | M2 | DONE |
| M4 | Git History Rewrite & Compression | Backup mirror/bundle, strip large blobs & historical junk apps, aggressive repack to <50 MB .git, pass git fsck | M3 | DONE |
| M5 | E2E Acceptance Verification & Audit | Verify all acceptance criteria (syntax, no broken links, secrets clean, git status clean, .git <50MB, git fsck) + Forensic Audit | M4 | DONE |

---

## Interface Contracts
### Hyprland ↔ Cursor & Wallpapers
- Cursor theme name: `MacOS-Tahoe-Cursor`, size `16` (invoked via `hyprctl setcursor MacOS-Tahoe-Cursor 16`).
- Fallback pointer: `.icons/default/index.theme` inherits `MacOS-Tahoe-Cursor`.
- Active wallpaper: `.config/hypr/wallpapers/current.jpg` exists and is referenced by `hyprlock.conf`.

### GTK ↔ Qt ↔ Theming
- GTK-3.0 & GTK-4.0: `gtk-icon-theme-name=MacTahoe-grey`, `gtk-cursor-theme-name=MacOS-Tahoe-Cursor`.
- Qt5 & Qt6: `icon_theme=MacTahoe-grey`.

### Git Working Tree ↔ Repository
- Working tree: Must contain only valid dotfiles and active themes (`.config/`, `.icons/{MacOS-Tahoe-Cursor,default,MacTahoe-grey}`, `assets/`, `README.md`, `.gitignore`).
- Git index: No untracked junk, no OS/editor/cache files, `git status` clean.
- Git database: `.git` directory < 50 MB, `git fsck --full` exits 0.

---

## Code Layout
- `/home/onicuto/.dotfiles/.config/hypr/`: Hyprland configuration files
- `/home/onicuto/.dotfiles/.config/waybar/`: Waybar status bar config and stylesheets
- `/home/onicuto/.dotfiles/.config/fish/`: Fish shell configuration and functions
- `/home/onicuto/.dotfiles/.config/ghostty/`: Ghostty terminal configuration
- `/home/onicuto/.dotfiles/.config/nvim/`: Neovim LazyVim configuration
- `/home/onicuto/.dotfiles/.config/cava/`: Cava audio visualizer configuration and shaders
- `/home/onicuto/.dotfiles/.config/neofetch/`: System information script configuration
- `/home/onicuto/.dotfiles/.config/fastfetch/`: Fastfetch configuration
- `/home/onicuto/.dotfiles/.icons/`: Cursor and icon themes (`MacOS-Tahoe-Cursor`, `default`, `MacTahoe-grey`)
- `/home/onicuto/.dotfiles/.gitignore`: Production repository ignore rules
- `/home/onicuto/.dotfiles/README.md`: Dotfiles documentation
