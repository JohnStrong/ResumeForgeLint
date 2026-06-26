import re
from collections.abc import Callable

from resumeforgelint.models import ScoredSection, Section, ScoringRubric, Issue, Severity


_FULL_NAME_TWO_WORD_BASIC_PATTERN =  re.compile(
    r"^(?:(?:Mr|Mrs|Miss|Ms|Dr|Prof)\.?\s+)?"           # optional prefix
    r"[A-ZÀ-Ž][a-zà-ž'-]+"                              # first name (accents, hyphens, apostrophes)
    r"(?:\s[A-ZÀ-Ž][a-zà-ž'-]+)+"                       # one or more additional name parts
    r"(?:\s(?:Jr|Sr|II|III|IV|PhD|MD|Esq)\.?)?$",       # optional suffix
    re.IGNORECASE                                       # handles ALL CAPS resumes
)

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Matches: 7-15 digit phone numbers with common separators (spaces, dots, dashes, parens)
# Covers: US (555-123-4567), UK (07700 900000), EU (06 12 34 56 78), international (+353 1 234 5678)
# Does NOT guard against: dates, zip codes, or other numeric sequences of similar length
PHONE_PATTERN = re.compile(r"\+?[\d\s.\-()]{7,15}\d")

def _match(section: Section, filter: Callable[[Section], list[str]], predicate: Callable[[str], bool]) -> bool:
    if not section.content:
        return False
    for line in filter(section):
        res = predicate(line)
        if res:
            return True
    return False        

def _contains_full_name_at_start(section: Section) -> bool:
    return _match(
        section=section, 
        filter=lambda s: [s.content[0].strip()],
        predicate=lambda line: bool(_FULL_NAME_TWO_WORD_BASIC_PATTERN.match(line))
    )

def _contains_email(section: Section) -> bool:
    return _match(
        section=section,
        filter=lambda s: s.content[1:],
        predicate=lambda line: bool(EMAIL_PATTERN.search(line))
    )

def _contains_phone_number(section: Section) -> bool:
    return _match(
        section=section,
        filter=lambda s: s.content[1:],
        predicate=lambda line: bool(PHONE_PATTERN.search(line))
    )

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
    ),
    ScoringRubric(
        title="PhoneNumberPresent",
        severity=Severity.CRITICAL,
        scorer=_contains_phone_number,
        message="A Phone Number should be within the Resume heading",
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
