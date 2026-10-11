"""Shared helper utilities and fixtures for dotfiles E2E test suite."""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path("/home/onicuto/.dotfiles").resolve()
HOME_DIR = Path("/home/onicuto").resolve()

# Secret detection regex patterns
SECRET_PATTERNS: Dict[str, re.Pattern] = {
    "Private Key": re.compile(
        r"-----BEGIN\s+(RSA|DSA|EC|OPENSSH|PGP)\s+PRIVATE\s+KEY-----",
        re.IGNORECASE,
    ),
    "GitHub Token (ghp/gho/pat)": re.compile(
        r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}|github_pat_[A-Za-z0-9_]{22,}",
    ),
    "AWS Access Key ID": re.compile(
        r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
    ),
    "Slack Token": re.compile(
        r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*",
    ),
    "Google API Key": re.compile(
        r"AIza[0-9A-Za-z\-_]{35}",
    ),
    "OpenAI API Key": re.compile(
        r"sk-[a-zA-Z0-9]{20,}",
    ),
    "HuggingFace Token": re.compile(
        r"hf_[a-zA-Z0-9]{34,}",
    ),
    "Telegram Bot Token": re.compile(
        r"[0-9]{8,10}:[a-zA-Z0-9_-]{35}",
    ),
    "Generic Password / Secret Assignment": re.compile(
        r"""(?i)(?:password|passwd|secret_key|auth_token)\s*[:=]\s*["']([^"'\s]{8,})["']""",
    ),
}


def run_command(
    cmd: str,
    cwd: Optional[Path] = None,
    timeout: int = 60,
    check: bool = False,
) -> subprocess.CompletedProcess:
    """Execute shell command and return CompletedProcess."""
    work_dir = str(cwd if cwd else REPO_ROOT)
    return subprocess.run(
        cmd,
        cwd=work_dir,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=check,
    )


def get_dir_size_bytes(dir_path: Path) -> int:
    """Calculate total size of directory in bytes."""
    total = 0
    if not dir_path.is_dir():
        return 0
    for root, _, files in os.walk(dir_path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                # Do not follow broken symlinks
                stat = os.lstat(fp)
                total += stat.st_size
            except (OSError, FileNotFoundError):
                pass
    return total


def scan_file_for_secrets(file_path: Path) -> List[Tuple[str, int, str]]:
    """Scan single file for secrets. Returns list of (pattern_name, line_no, matched_preview)."""
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                # Skip comments that document patterns or tests
                stripped = line.strip()
                if stripped.startswith("#") and "pattern" in stripped.lower():
                    continue
                for name, pat in SECRET_PATTERNS.items():
                    m = pat.search(line)
                    if m:
                        preview = m.group(0)
                        findings.append((name, line_no, preview))
    except Exception:
        pass
    return findings


def get_git_objects_with_sizes(cwd: Optional[Path] = None) -> List[Dict[str, any]]:
    """Enumerate all git objects across all refs with size and path."""
    work_dir = cwd if cwd else REPO_ROOT
    proc = subprocess.run(
        "git rev-list --objects --all",
        cwd=work_dir,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )
    objects_input = proc.stdout
    if not objects_input.strip():
        return []

    cat_proc = subprocess.run(
        "git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(rest)'",
        input=objects_input,
        cwd=work_dir,
        shell=True,
        capture_output=True,
        text=True,
        check=True,
    )

    results = []
    for line in cat_proc.stdout.splitlines():
        parts = line.split(maxsplit=3)
        if len(parts) >= 3:
            sha, obj_type, size_str = parts[0], parts[1], parts[2]
            path = parts[3] if len(parts) > 3 else ""
            try:
                size = int(size_str)
            except ValueError:
                continue
            results.append({
                "sha": sha,
                "type": obj_type,
                "size": size,
                "path": path,
            })
    return results
