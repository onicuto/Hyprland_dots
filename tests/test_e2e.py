#!/usr/bin/env python3
"""Unified E2E Test Runner for Dotfiles Audit and Optimization (Requirements R1 - R4).

Usage:
    python3 tests/test_e2e.py [--tier {r1,r2,r3,r4,all}] [--verbose] [--json] [--failfast]

Exit codes:
    0: All executed tests passed.
    1: One or more tests failed.
"""

import argparse
import io
import json
import os
import sys
import time
import unittest
from pathlib import Path
from typing import Dict, List, Optional

# Ensure repository root is in python path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests.test_r1_configs import (
    TestR1FishScripts,
    TestR1WaybarConfig,
    TestR1HyprlandConfig,
    TestR1SystemFetchersAndDocumentation,
    TestR1SecretScan,
)
from tests.test_r2_gitignore import (
    TestR2Gitignore,
)
from tests.test_r3_git_history import (
    TestR3GitHistory,
)
from tests.test_r4_icons import (
    TestR4Icons,
)

# Colors for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE = "\033[37m"

REQUIREMENTS_MAP = {
    "R1": {
        "title": "R1: Configuration Syntax, Links & Secrets Audit",
        "suites": [
            TestR1FishScripts,
            TestR1WaybarConfig,
            TestR1HyprlandConfig,
            TestR1SystemFetchersAndDocumentation,
            TestR1SecretScan,
        ],
    },
    "R2": {
        "title": "R2: Production .gitignore & Working Tree Cleanliness",
        "suites": [
            TestR2Gitignore,
        ],
    },
    "R3": {
        "title": "R3: Git History Purge, Compression (<50MB) & Integrity",
        "suites": [
            TestR3GitHistory,
        ],
    },
    "R4": {
        "title": "R4: Local Assets (.icons) Theme Optimization & Symlinks",
        "suites": [
            TestR4Icons,
        ],
    },
}


def build_suite_for_requirement(req_key: str) -> unittest.TestSuite:
    """Build a TestSuite for a single requirement key (e.g. 'R1')."""
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    req_info = REQUIREMENTS_MAP.get(req_key)
    if req_info:
        for cls in req_info["suites"]:
            suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


def run_tier(
    tier_key: str,
    verbose: bool = False,
    failfast: bool = False,
) -> Dict[str, any]:
    """Execute tests for a specific requirement or all requirements."""
    selected_keys = (
        [tier_key.upper()]
        if tier_key.upper() in REQUIREMENTS_MAP
        else list(REQUIREMENTS_MAP.keys())
    )

    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tier": tier_key,
        "requirements": {},
        "total_tests": 0,
        "total_passed": 0,
        "total_failed": 0,
        "total_errors": 0,
        "duration_seconds": 0.0,
        "success": True,
    }

    start_total_time = time.time()

    for req_key in selected_keys:
        req_meta = REQUIREMENTS_MAP[req_key]
        suite = build_suite_for_requirement(req_key)

        stream = io.StringIO()
        runner = unittest.TextTestRunner(
            stream=stream,
            verbosity=2 if verbose else 1,
            failfast=failfast,
        )

        req_start = time.time()
        test_result = runner.run(suite)
        req_duration = time.time() - req_start

        tests_run = test_result.testsRun
        failures_count = len(test_result.failures)
        errors_count = len(test_result.errors)
        passed_count = tests_run - (failures_count + errors_count)
        is_success = test_result.wasSuccessful()

        failures_detail = []
        for test, trace in test_result.failures:
            failures_detail.append({
                "test": str(test),
                "type": "FAILURE",
                "message": trace.strip().splitlines()[-1] if trace else "Assertion failed",
                "traceback": trace,
            })
        for test, trace in test_result.errors:
            failures_detail.append({
                "test": str(test),
                "type": "ERROR",
                "message": trace.strip().splitlines()[-1] if trace else "Runtime error",
                "traceback": trace,
            })

        results["requirements"][req_key] = {
            "title": req_meta["title"],
            "tests_run": tests_run,
            "passed": passed_count,
            "failed": failures_count,
            "errors": errors_count,
            "duration_seconds": round(req_duration, 3),
            "success": is_success,
            "issues": failures_detail,
        }

        results["total_tests"] += tests_run
        results["total_passed"] += passed_count
        results["total_failed"] += failures_count
        results["total_errors"] += errors_count

        if not is_success:
            results["success"] = False
            if failfast:
                break

    results["duration_seconds"] = round(time.time() - start_total_time, 3)
    return results


def print_formatted_report(results: Dict[str, any], verbose: bool = False):
    """Print clean ANSI-colored report to console."""
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}        DOTFILES E2E TEST SUITE EXECUTION REPORT (R1 - R4)            {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    print(f"{BOLD}Execution Timestamp:{RESET} {results['timestamp']}")
    print(f"{BOLD}Target Scope:{RESET}        {results['tier'].upper()}")
    print(f"{BOLD}Total Duration:{RESET}      {results['duration_seconds']}s\n")

    print(f"{BOLD}{WHITE}{'Req':<6} {'Status':<10} {'Passed':<8} {'Failed':<8} {'Duration':<10} {'Description'}{RESET}")
    print("-" * 78)

    for req_key, data in results["requirements"].items():
        if data["success"]:
            status_str = f"{GREEN}{BOLD}PASS{RESET}"
        else:
            status_str = f"{RED}{BOLD}FAIL{RESET}"

        duration_str = f"{data['duration_seconds']}s"
        print(
            f"{BOLD}{req_key:<6}{RESET} {status_str:<19} "
            f"{GREEN}{data['passed']:<8}{RESET} "
            f"{(RED + str(data['failed'] + data['errors']) + RESET):<17} "
            f"{duration_str:<10} "
            f"{data['title']}"
        )

    print("-" * 78)
    summary_color = GREEN if results["success"] else RED
    summary_status = "ALL TESTS PASSED (ACCEPTANCE CRITERIA MET)" if results["success"] else "FAILURES DETECTED (DEFECTS ESCALATED)"
    print(
        f"\n{BOLD}Summary:{RESET} {summary_color}{BOLD}{summary_status}{RESET} "
        f"({results['total_passed']}/{results['total_tests']} tests passed)\n"
    )

    # Detailed issue breakdown
    has_issues = False
    for req_key, data in results["requirements"].items():
        if data["issues"]:
            if not has_issues:
                print(f"{BOLD}{RED}--- DETAILED DEFECT BREAKDOWN ---{RESET}\n")
                has_issues = True
            print(f"{BOLD}{YELLOW}[{req_key}] {data['title']}:{RESET}")
            for issue in data["issues"]:
                print(f"  • {RED}{issue['test']}{RESET}:")
                print(f"    {issue['message']}")
                if verbose:
                    print(f"\n{WHITE}{issue['traceback']}{RESET}\n")
            print()


def main():
    parser = argparse.ArgumentParser(description="Dotfiles Acceptance Test Runner (R1 - R4)")
    parser.add_argument(
        "--tier",
        "-t",
        choices=["r1", "r2", "r3", "r4", "all"],
        default="all",
        help="Specify requirement tier to run (default: all)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose test outputs and full stack traces",
    )
    parser.add_argument(
        "--failfast",
        "-f",
        action="store_true",
        help="Stop on first failure",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON results for CI integration",
    )

    args = parser.parse_args()
    results = run_tier(tier_key=args.tier, verbose=args.verbose, failfast=args.failfast)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_formatted_report(results, verbose=args.verbose)

    sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()
