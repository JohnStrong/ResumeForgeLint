"""Fidelity test: compare spaCy NER extraction against ResumeForgeLint scoring output.

Asserts that when spaCy can extract a field, our tool scores it as passing,
and when spaCy cannot extract it, our tool flags it as an issue.

Run: python scripts/fidelity_test.py

Requires: pip install spacy && python -m spacy download en_core_web_sm
"""
import re
import sys
from pathlib import Path

import spacy

from resumeforgelint.cli import _validate

nlp = spacy.load("en_core_web_sm")

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"\+?[\d\s.\-()]{7,15}\d")
DATE_RE = re.compile(
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+)?\d{4}"
    r"\s*[-–—]\s*"
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+)?(\d{4}|[Pp]resent)",
    re.IGNORECASE,
)
DEGREE_RE = re.compile(
    r"\b(B\.?Sc|M\.?Sc|Ph\.?D|B\.?A|M\.?A|MBA|B\.?Eng|M\.?Eng|Bachelor|Master|Doctorate)\b",
    re.IGNORECASE,
)
INSTITUTION_RE = re.compile(r"\b(University|College|Institute|School|Academy)\b", re.IGNORECASE)

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


def spacy_extract(text: str) -> dict:
    """Extract structured data using spaCy NLP (control)."""
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return {
        "has_name": any(len(n.split()) >= 2 for n in names),
        "has_email": bool(EMAIL_RE.search(text)),
        "has_phone": bool(PHONE_RE.search(text)),
        "has_org": any(ent.label_ == "ORG" for ent in doc.ents),
        "has_dates": bool(DATE_RE.search(text)),
        "has_degree": bool(DEGREE_RE.search(text)),
        "has_institution": bool(INSTITUTION_RE.search(text)),
    }


def parse_lint_output(output: str) -> dict:
    """Parse ResumeForgeLint output to extract per-section scores (test)."""
    sections = {}
    for line in output.splitlines():
        # Match lines like: "  Header             🟢  20/20  "
        match = re.match(r"\s+(\S+)\s+[🟢🟡🔴]\s+(\d+)/20\s*(.*)", line)
        if match:
            name = match.group(1)
            score = int(match.group(2))
            issue = match.group(3).strip()
            sections[name.lower()] = {"score": score, "issue": issue}
    return sections


def assert_alignment(filename: str, spacy_data: dict, lint_sections: dict) -> list[str]:
    """Compare spaCy extraction against lint scores. Returns list of mismatches."""
    mismatches = []

    # Header checks
    header = lint_sections.get("header", {})
    header_score = header.get("score", 0)
    header_full = header_score >= 15  # allow for missing country code warning

    if spacy_data["has_name"] and spacy_data["has_email"] and spacy_data["has_phone"]:
        if not header_full:
            mismatches.append(f"spaCy found name+email+phone but lint scored Header {header_score}/20")
    if not spacy_data["has_name"] and header_score > 10:
        mismatches.append(f"spaCy could NOT find name but lint scored Header {header_score}/20")

    # Experience checks
    exp = lint_sections.get("experience", {})
    exp_score = exp.get("score", 0)

    if spacy_data["has_org"] and spacy_data["has_dates"]:
        if exp_score < 10:
            mismatches.append(f"spaCy found org+dates but lint scored Experience {exp_score}/20")
    if not spacy_data["has_org"] and not spacy_data["has_dates"] and exp_score > 5:
        mismatches.append(f"spaCy found NO org/dates but lint scored Experience {exp_score}/20")

    # Education checks
    edu = lint_sections.get("education", {})
    edu_score = edu.get("score", 0)

    if spacy_data["has_degree"] and spacy_data["has_institution"]:
        if edu_score < 10:
            mismatches.append(f"spaCy found degree+institution but lint scored Education {edu_score}/20")
    if not spacy_data["has_degree"] and not spacy_data["has_institution"] and edu_score > 11:
        mismatches.append(f"spaCy found NO degree/institution but lint scored Education {edu_score}/20")

    return mismatches


def main():
    trace = "--trace" in sys.argv
    files = ["good_header.txt", "bad_all.txt", "needs_work.txt"]
    total_failures = 0

    for filename in files:
        filepath = EXAMPLES_DIR / filename
        text = filepath.read_text()

        # Control: spaCy extraction
        spacy_data = spacy_extract(text)

        # Test: ResumeForgeLint output
        lint_output = _validate(text)
        lint_sections = parse_lint_output(lint_output)

        # Compare
        mismatches = assert_alignment(filename, spacy_data, lint_sections)

        print(f"=== {filename} ===")
        if trace:
            print(f"  [spaCy control]")
            for k, v in spacy_data.items():
                print(f"    {k}: {v}")
            print(f"  [ResumeForgeLint test]")
            for section, data in lint_sections.items():
                print(f"    {section}: {data['score']}/20  {data['issue'] or '(no issues)'}")
            print(f"  [Comparison]")
        if mismatches:
            for m in mismatches:
                print(f"  ✗ MISMATCH: {m}")
            total_failures += len(mismatches)
        else:
            print(f"  ✓ ALIGNED")
        print()

    if total_failures:
        print(f"FAILED: {total_failures} mismatch(es) found.")
        sys.exit(1)
    else:
        print("PASSED: All ResumeForgeLint scores align with spaCy NER extraction.")


if __name__ == "__main__":
    main()
