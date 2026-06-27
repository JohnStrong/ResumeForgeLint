import re

from resumeforgelint.models import Section, ScoringRubric, Severity


# Matches degree types: BSc, MSc, PhD, BA, MA, MBA, BEng, MEng, etc.
_DEGREE_PATTERN = re.compile(
    r"\b(B\.?Sc|M\.?Sc|Ph\.?D|B\.?A|M\.?A|MBA|B\.?Eng|M\.?Eng|"
    r"Bachelor|Master|Doctorate|Associate|Diploma)\b",
    re.IGNORECASE,
)

# Matches institution indicators: "University", "College", "Institute", "School"
_INSTITUTION_PATTERN = re.compile(
    r"\b(University|College|Institute|School|Academy|Polytechnic)\b",
    re.IGNORECASE,
)

# Matches a 4-digit year (graduation date)
_GRADUATION_DATE_PATTERN = re.compile(r"\b(19|20)\d{2}\b")


def _section_present(section: Section) -> bool:
    return len(section.content) > 0


def _has_degree_type(section: Section) -> bool:
    for line in section.content:
        if _DEGREE_PATTERN.search(line):
            return True
    return False


def _has_institution(section: Section) -> bool:
    for line in section.content:
        if _INSTITUTION_PATTERN.search(line):
            return True
    return False


def _has_graduation_date(section: Section) -> bool:
    for line in section.content:
        if _GRADUATION_DATE_PATTERN.search(line):
            return True
    return False


RUBRICS: list[ScoringRubric] = [
    ScoringRubric(
        title="SectionPresent",
        severity=Severity.CRITICAL,
        scorer=_section_present,
        message="Education section should not be empty",
        points=11,
    ),
    ScoringRubric(
        title="DegreeTypePresent",
        severity=Severity.CRITICAL,
        scorer=_has_degree_type,
        message="Education should include a degree type (e.g. BSc, MSc, PhD)",
        points=6,
    ),
    ScoringRubric(
        title="InstitutionPresent",
        severity=Severity.CRITICAL,
        scorer=_has_institution,
        message="Education should include the institution name",
        points=5,
    ),
    ScoringRubric(
        title="GraduationDatePresent",
        severity=Severity.WARNING,
        scorer=_has_graduation_date,
        message="Education should include a graduation date",
        points=4,
    ),
]
