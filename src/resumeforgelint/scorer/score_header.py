import re

from resumeforgelint.models import ScoredSection, Section, ScoringRubric, Issue, Severity


_FULL_NAME_TWO_WORD_BASIC_PATTERN =  re.compile(
    r"^(?:(?:Mr|Mrs|Miss|Ms|Dr|Prof)\.?\s+)?"           # optional prefix
    r"[A-ZÀ-Ž][a-zà-ž'-]+"                              # first name (accents, hyphens, apostrophes)
    r"(?:\s[A-ZÀ-Ž][a-zà-ž'-]+)+"                       # one or more additional name parts
    r"(?:\s(?:Jr|Sr|II|III|IV|PhD|MD|Esq)\.?)?$",       # optional suffix
    re.IGNORECASE                                       # handles ALL CAPS resumes
)

def _contains_full_name_at_start(section: Section) -> bool:
    if not section.content:
        return False
    return bool(_FULL_NAME_TWO_WORD_BASIC_PATTERN.match(section.content[0].strip()))


RUBRICS: list[ScoringRubric] = [
    ScoringRubric(
        title="FullNameRubric",
        severity=Severity.CRITICAL,
        scorer=_contains_full_name_at_start,
        message="A Resume should contain the applicants full name at the start (top) of the document",
        points=10,
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
    return ScoredSection(section=section, score=points, issues=issues)
