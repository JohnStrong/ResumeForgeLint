import re

from resumeforgelint.models import Section, ScoringRubric, Severity


# Common technical keywords found in skills sections
_TECHNICAL_KEYWORDS = re.compile(
    r"\b("
    r"python|java|javascript|typescript|c\+\+|c#|go|rust|ruby|swift|kotlin|php|scala|"
    r"sql|html|css|react|angular|vue|node|django|flask|spring|"
    r"aws|azure|gcp|docker|kubernetes|terraform|jenkins|git|linux|"
    r"api|rest|graphql|microservices|ci/cd|agile|scrum|"
    r"machine learning|deep learning|data science|"
    r"postgresql|mysql|mongodb|redis|dynamodb|elasticsearch"
    r")\b",
    re.IGNORECASE,
)

_MIN_KEYWORD_COUNT = 5

# Common soft-skill filler words that dilute a skills section
_SOFT_SKILL_FILLER = re.compile(
    r"\b(team player|hard worker|self-starter|motivated|passionate|"
    r"detail-oriented|fast learner|go-getter|synergy|proactive)\b",
    re.IGNORECASE,
)


def _section_present(section: Section) -> bool:
    return len(section.content) > 0


def _contains_technical_keywords(section: Section) -> bool:
    for line in section.content:
        if _TECHNICAL_KEYWORDS.search(line):
            return True
    return False


def _meets_minimum_keyword_count(section: Section) -> bool:
    count = 0
    for line in section.content:
        count += len(_TECHNICAL_KEYWORDS.findall(line))
    return count >= _MIN_KEYWORD_COUNT


def _no_excessive_soft_skill_filler(section: Section) -> bool:
    filler_count = 0
    for line in section.content:
        filler_count += len(_SOFT_SKILL_FILLER.findall(line))
    return filler_count == 0


RUBRICS: list[ScoringRubric] = [
    ScoringRubric(
        title="SectionPresent",
        severity=Severity.CRITICAL,
        scorer=_section_present,
        message="Skills section should not be empty",
        points=11,
    ),
    ScoringRubric(
        title="ContainsTechnicalKeywords",
        severity=Severity.CRITICAL,
        scorer=_contains_technical_keywords,
        message="Skills section should contain technical keywords (tools, languages, frameworks)",
        points=6,
    ),
    ScoringRubric(
        title="MinimumKeywordCount",
        severity=Severity.WARNING,
        scorer=_meets_minimum_keyword_count,
        message=f"Skills section should list at least {_MIN_KEYWORD_COUNT} technical keywords",
        points=3,
    ),
    ScoringRubric(
        title="NoSoftSkillFiller",
        severity=Severity.WARNING,
        scorer=_no_excessive_soft_skill_filler,
        message="Skills section should avoid soft-skill filler (e.g. 'team player', 'hard worker')",
        points=3,
    ),
]
