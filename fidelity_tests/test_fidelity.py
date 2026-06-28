"""Fidelity tests: assert spaCy NER extraction aligns with ResumeForgeLint scoring.

When spaCy can extract a field, our tool should score it as passing.
When spaCy cannot extract it, our tool should flag it as an issue.

Requires: pip install spacy && python -m spacy download en_core_web_sm
"""
import re
from pathlib import Path

import pytest
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


def _spacy_extract(text: str) -> dict:
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


def _parse_lint_output(output: str) -> dict:
    sections = {}
    for line in output.splitlines():
        match = re.match(r"\s+(\S+)\s+[🟢🟡🔴]\s+(\d+)/20\s*(.*)", line)
        if match:
            name = match.group(1).lower()
            score = int(match.group(2))
            sections[name] = score
    return sections


class TestFidelityHeader:
    def test_good_header_name_found_scores_high(self):
        """FIDELITY: spaCy finds name → header scores >= 15."""
        text = (EXAMPLES_DIR / "good_header.txt").read_text()
        spacy_data = _spacy_extract(text)
        lint = _parse_lint_output(_validate(text))
        assert spacy_data["has_name"] is True
        assert lint["header"] >= 15

    def test_bad_header_name_not_found_scores_low(self):
        """FIDELITY: spaCy cannot find name → header scores low."""
        text = (EXAMPLES_DIR / "bad_all.txt").read_text()
        spacy_data = _spacy_extract(text)
        lint = _parse_lint_output(_validate(text))
        assert spacy_data["has_name"] is False
        assert lint["header"] <= 10


class TestFidelityExperience:
    def test_good_experience_org_and_dates_found(self):
        """FIDELITY: spaCy finds org+dates → experience scores >= 10."""
        text = (EXAMPLES_DIR / "good_header.txt").read_text()
        spacy_data = _spacy_extract(text)
        lint = _parse_lint_output(_validate(text))
        assert spacy_data["has_org"] is True
        assert spacy_data["has_dates"] is True
        assert lint["experience"] >= 10

    def test_bad_experience_no_org_no_dates(self):
        """FIDELITY: spaCy finds no org/dates → experience scores <= 5."""
        text = (EXAMPLES_DIR / "bad_all.txt").read_text()
        spacy_data = _spacy_extract(text)
        lint = _parse_lint_output(_validate(text))
        assert spacy_data["has_org"] is False
        assert spacy_data["has_dates"] is False
        assert lint["experience"] <= 5


class TestFidelityEducation:
    def test_good_education_degree_and_institution_found(self):
        """FIDELITY: spaCy finds degree+institution → education scores >= 10."""
        text = (EXAMPLES_DIR / "good_header.txt").read_text()
        spacy_data = _spacy_extract(text)
        lint = _parse_lint_output(_validate(text))
        assert spacy_data["has_degree"] is True
        assert spacy_data["has_institution"] is True
        assert lint["education"] >= 10

    def test_bad_education_no_degree_no_institution(self):
        """FIDELITY: spaCy finds no degree/institution → education scores low."""
        text = (EXAMPLES_DIR / "needs_work.txt").read_text()
        spacy_data = _spacy_extract(text)
        lint = _parse_lint_output(_validate(text))
        assert spacy_data["has_degree"] is False
        assert spacy_data["has_institution"] is False
        assert lint["education"] <= 10


class TestFidelitySkills:
    def test_good_skills_scores_high(self):
        """FIDELITY: resume with technical keywords → skills scores >= 15."""
        text = (EXAMPLES_DIR / "good_header.txt").read_text()
        lint = _parse_lint_output(_validate(text))
        assert lint["skills"] >= 15

    def test_bad_skills_no_keywords_scores_low(self):
        """FIDELITY: resume with only soft skills → skills scores low."""
        text = (EXAMPLES_DIR / "bad_skills.txt").read_text()
        lint = _parse_lint_output(_validate(text))
        assert lint["skills"] <= 10
