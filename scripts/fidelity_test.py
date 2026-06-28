"""Fidelity test: compare spaCy NER extraction against ResumeForgeLint scoring.

Run: python scripts/fidelity_test.py

Requires: pip install spacy && python -m spacy download en_core_web_sm
"""
import re
from pathlib import Path

import spacy

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


def extract(filepath: Path) -> dict:
    text = filepath.read_text()
    doc = nlp(text)

    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    dates = DATE_RE.findall(text)
    degrees = DEGREE_RE.findall(text)
    institutions = INSTITUTION_RE.findall(text)

    return {
        "name": names[0] if names else None,
        "email": emails[0] if emails else None,
        "phone": phones[0].strip() if phones else None,
        "orgs": orgs or None,
        "date_ranges": len(dates),
        "degree": degrees[0] if degrees else None,
        "institution": institutions[0] if institutions else None,
    }


def main():
    files = ["good_header.txt", "bad_header.txt", "bad_all.txt", "needs_work.txt"]

    for f in files:
        filepath = EXAMPLES_DIR / f
        print(f"=== {f} ===")
        data = extract(filepath)

        print(f"  [Header]")
        print(f"    Name:        {data['name'] or 'NOT FOUND'}")
        print(f"    Email:       {data['email'] or 'NOT FOUND'}")
        print(f"    Phone:       {data['phone'] or 'NOT FOUND'}")
        print(f"  [Experience]")
        print(f"    Orgs:        {data['orgs'] or 'NOT FOUND'}")
        print(f"    Date ranges: {data['date_ranges']}")
        print(f"  [Education]")
        print(f"    Degree:      {data['degree'] or 'NOT FOUND'}")
        print(f"    Institution: {data['institution'] or 'NOT FOUND'}")
        print()


if __name__ == "__main__":
    main()
