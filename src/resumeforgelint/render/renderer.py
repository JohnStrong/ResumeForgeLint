from resumeforgelint.models import ScoredSection, Issue, Severity
from resumeforgelint.render.template_engine import TemplateEngine

SECTION_MAX_SCORE = 20

_SEVERITY_ORDER = {Severity.CRITICAL: 0, Severity.WARNING: 1, Severity.INFO: 2}

def _score_to_visual_rating(score: int, max_score: int) -> tuple[str, str]:
    normalized_score = score / max_score
    if normalized_score >= 0.8:
        return ("🟢", "Good")
    if normalized_score >= 0.5:
        return ("🟡", "Needs Work")
    return ("🔴", "Poor")

def _severity_to_icon(severity: Severity) -> str:
    if severity == Severity.CRITICAL:
        return "✖"
    if severity == Severity.WARNING:
        return "⚠"
    return "i"

def _transform_issues(issues: list[Issue], limit: int = 1) -> str:
    sorted_issues = sorted(issues, key=lambda i: _SEVERITY_ORDER[i.severity])
    top_issues = sorted_issues[:limit]
    return ", ".join(f"{_severity_to_icon(i.severity)} {i.message}" for i in top_issues)

def _transform_summary(scored_sections: list[ScoredSection]) -> dict[str, str]:
    total_score = sum(s.score for s in scored_sections)
    max_score = len(scored_sections) * SECTION_MAX_SCORE
    emoji, rating = _score_to_visual_rating(total_score, max_score)
    return {"emoji": emoji, "rating": rating, "total": str(total_score), "max": str(max_score)}

def _transform_section(scored_section: ScoredSection) -> dict[str, str]:
    emoji, _ = _score_to_visual_rating(scored_section.score, max_score=SECTION_MAX_SCORE)
    return {
        "name": scored_section.section.heading or "Header",
        "emoji": emoji,
        "score": scored_section.score,
        "issues": _transform_issues(scored_section.issues),
    }

def render(scored_sections: list[ScoredSection]) -> str:
    """Takes scored sections, transforms and renders via the template engine."""
    engine = TemplateEngine().summary(_transform_summary(scored_sections))
    for section in scored_sections:
        engine.section(_transform_section(section))
    return engine.render()
