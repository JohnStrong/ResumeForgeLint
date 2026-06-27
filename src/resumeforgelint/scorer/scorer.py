from resumeforgelint.models import ScoredSection, Section, ScoringRubric, Issue

def score(section: Section, rubrics: list[ScoringRubric]) -> ScoredSection:
    points: int = 20
    issues: list[Issue] = []
    for rubric in rubrics:
        result = rubric.scorer(section)
        if not result:
            points -= rubric.points
            issues.append(Issue(severity=rubric.severity, message=rubric.message))
    return ScoredSection(section=section, score=max(points, 0), issues=issues)
