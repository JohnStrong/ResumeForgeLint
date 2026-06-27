import re

from resumeforgelint.models import Section, ScoringRubric, Severity


# Matches numbers, percentages, dollar amounts, metrics (e.g. "50%", "$1.2M", "3x", "100+")
_QUANTIFIED_PATTERN = re.compile(r"\d+[%xX]|\$[\d,.]+[KMBkmb]?|\d{2,}")

# Common action verbs that start bullet points in work experience
_ACTION_VERBS = {
    "achieved", "built", "created", "delivered", "designed", "developed",
    "drove", "enabled", "engineered", "established", "executed", "expanded",
    "grew", "implemented", "improved", "increased", "launched", "led",
    "managed", "migrated", "optimized", "orchestrated", "owned", "pioneered",
    "reduced", "refactored", "scaled", "shipped", "spearheaded", "streamlined",
    "transformed", "upgraded",
}

# Matches date ranges like "2020 - 2024", "Jan 2020 - Present", "2020-Present"
_DATE_RANGE_PATTERN = re.compile(
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+)?\d{4}"
    r"\s*[-–—]\s*"
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+)?(\d{4}|[Pp]resent)",
    re.IGNORECASE,
)

# Matches "Company - Role" or "Role at Company" patterns (line with a dash or "at")
_COMPANY_ROLE_PATTERN = re.compile(r".+\s[-–—]\s.+|.+\s+at\s+.+", re.IGNORECASE)


def _section_present(section: Section) -> bool:
    return len(section.content) > 0


def _has_quantified_achievements(section: Section) -> bool:
    for line in section.content:
        if _QUANTIFIED_PATTERN.search(line):
            return True
    return False


def _has_action_verbs(section: Section) -> bool:
    for line in section.content:
        stripped = line.strip().lstrip("•-–▪▸► ")
        first_word = stripped.split()[0].lower() if stripped.split() else ""
        if first_word in _ACTION_VERBS:
            return True
    return False


def _has_date_ranges(section: Section) -> bool:
    for line in section.content:
        if _DATE_RANGE_PATTERN.search(line):
            return True
    return False


def _has_company_and_role(section: Section) -> bool:
    for line in section.content:
        if _COMPANY_ROLE_PATTERN.match(line.strip()):
            return True
    return False


RUBRICS: list[ScoringRubric] = [
    ScoringRubric(
        title="SectionPresent",
        severity=Severity.CRITICAL,
        scorer=_section_present,
        message="Work Experience section should not be empty",
        points=11,
    ),
    ScoringRubric(
        title="CompanyAndRolePresent",
        severity=Severity.CRITICAL,
        scorer=_has_company_and_role,
        message="Each role should include company name and role title",
        points=8,
    ),
    ScoringRubric(
        title="DateRangesPresent",
        severity=Severity.CRITICAL,
        scorer=_has_date_ranges,
        message="Each role should include date ranges (e.g. 2020 - Present)",
        points=6,
    ),
    ScoringRubric(
        title="QuantifiedAchievements",
        severity=Severity.WARNING,
        scorer=_has_quantified_achievements,
        message="Work Experience should include quantified achievements (numbers, percentages, metrics)",
        points=3,
    ),
    ScoringRubric(
        title="ActionVerbs",
        severity=Severity.WARNING,
        scorer=_has_action_verbs,
        message="Bullet points should start with strong action verbs (e.g. built, delivered, improved)",
        points=3,
    ),
]
