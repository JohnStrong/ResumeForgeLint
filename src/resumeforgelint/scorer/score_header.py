import re

from resumeforgelint.models import ScoredSection, Section, ScoringRubric, Issue, Severity


_FULL_NAME_TWO_WORD_BASIC_PATTERN =  re.compile(
    r"^(?:(?:Mr|Mrs|Miss|Ms|Dr|Prof)\.?\s+)?"           # optional prefix
    r"[A-ZÀ-Ž][a-zà-ž'-]+"                              # first name (accents, hyphens, apostrophes)
    r"(?:\s[A-ZÀ-Ž][a-zà-ž'-]+)+"                       # one or more additional name parts
    r"(?:\s(?:Jr|Sr|II|III|IV|PhD|MD|Esq)\.?)?$",       # optional suffix
    re.IGNORECASE                                       # handles ALL CAPS resumes
)

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def _contains_full_name_at_start(section: Section) -> bool:
    if not section.content:
        return False
    return bool(_FULL_NAME_TWO_WORD_BASIC_PATTERN.match(section.content[0].strip()))

def _contains_email(section: Section) -> bool:
    if not section.content:
        return False
    for line in section.content[1:]:  # skip first line (reserved for name)
        if EMAIL_PATTERN.search(line):
            return True
    return False

RUBRICS: list[ScoringRubric] = [
    ScoringRubric(
        title="FullNameRubric",
        severity=Severity.CRITICAL,
        scorer=_contains_full_name_at_start,
        message="A Resume should contain the applicants full name at the start (top) of the document",
        points=11,
    ),
    ScoringRubric(
        title="EmailAddressPresent",
        severity=Severity.CRITICAL,
        scorer=_contains_email,
        message="Email address should be within the Resume heading",
        points=11
    )
]

def score_header(section: Section) -> ScoredSection:
    points: int = 20
    issues: list[Issue] = []
    for rubric in RUBRICS:
        result = rubric.scorer(section)
        if not result:
            points -= rubric.points
            issues.append(Issue(severity=rubric.severity, message=rubric.message))
    return ScoredSection(section=section, score=max(points, 0), issues=issues)
