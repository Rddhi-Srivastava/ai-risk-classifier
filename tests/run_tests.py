"""
Runs every case in test_cases.py through the live classifier and prints/
writes an accuracy report.

Requires GEMINI_API_KEY to be set - this makes real API calls.

Usage:
    cd tests
    python run_tests.py
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from classifier import ClassificationError, classify_system
from test_cases import TEST_CASES

try:
    from google.genai.errors import ClientError
except ImportError:
    ClientError = None

REPORT_PATH = os.path.join(os.path.dirname(__file__), "accuracy_report.md")
SECONDS_BETWEEN_CALLS = 13  # free tier: 5 requests/minute -> stay under that
MAX_RATE_LIMIT_RETRIES = 3


def _classify_with_rate_limit_retry(description):
    for attempt in range(MAX_RATE_LIMIT_RETRIES):
        try:
            return classify_system(description)
        except Exception as e:
            is_rate_limit = ClientError is not None and isinstance(e, ClientError) and "429" in str(e)
            if is_rate_limit and attempt < MAX_RATE_LIMIT_RETRIES - 1:
                wait = 35
                print(f"(rate limited, waiting {wait}s before retry...)", end=" ", flush=True)
                time.sleep(wait)
                continue
            raise


def run() -> None:
    results = []
    correct = 0
    scored_cases = 0

    for case in TEST_CASES:
        print(f"[{case['id']}] classifying...", end=" ", flush=True)
        try:
            result = _classify_with_rate_limit_retry(case["description"])
            got_tier = result.tier
            flagged_borderline = result.borderline
        except (ClassificationError, Exception) as e:
            print(f"ERROR: {e}")
            results.append(
                {
                    **case,
                    "got_tier": "ERROR",
                    "flagged_borderline": None,
                    "pass": False,
                    "error": str(e),
                }
            )
            continue

        if case["expected_tier"] == "ambiguous":
            passed = flagged_borderline
            scored_cases += 1
        else:
            passed = got_tier == case["expected_tier"]
            scored_cases += 1

        if passed:
            correct += 1

        status = "PASS" if passed else "FAIL"
        print(f"{status} (expected={case['expected_tier']}, got={got_tier}, borderline={flagged_borderline})")

        results.append(
            {
                **case,
                "got_tier": got_tier,
                "flagged_borderline": flagged_borderline,
                "pass": passed,
                "reasoning": result.reasoning,
            }
        )
        time.sleep(SECONDS_BETWEEN_CALLS)

    accuracy = correct / scored_cases if scored_cases else 0
    _write_report(results, correct, scored_cases, accuracy)
    print(f"\n{correct}/{scored_cases} correct ({accuracy:.0%}). Report written to {REPORT_PATH}")


def _write_report(results, correct, total, accuracy) -> None:
    lines = [
        "# Accuracy Report",
        "",
        f"**{correct}/{total} correct ({accuracy:.0%})**",
        "",
        "First-pass triage test against a hand-written test set spanning all four",
        "EU AI Act risk tiers, including two deliberately ambiguous edge cases.",
        "",
        "| ID | Expected | Got | Pass | Notes |",
        "|----|----------|-----|------|-------|",
    ]
    for r in results:
        notes = r["notes"] if isinstance(r["notes"], str) else r["notes"]
        lines.append(
            f"| {r['id']} | {r['expected_tier']} | {r.get('got_tier', 'ERROR')} | "
            f"{'✅' if r['pass'] else '❌'} | {notes} |"
        )

    lines.append("")
    lines.append("## Full descriptions and model reasoning")
    for r in results:
        lines.append(f"\n### {r['id']} ({'PASS' if r['pass'] else 'FAIL'})")
        lines.append(f"- **Description:** {r['description']}")
        lines.append(f"- **Expected tier:** {r['expected_tier']}")
        lines.append(f"- **Model tier:** {r.get('got_tier', 'ERROR')}")
        if r.get("reasoning"):
            lines.append(f"- **Model reasoning:** {r['reasoning']}")
        if r.get("error"):
            lines.append(f"- **Error:** {r['error']}")

    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    run()