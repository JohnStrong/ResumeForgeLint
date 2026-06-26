import pytest

from resumeforgelint.models import Section, SectionType, ScoredSection, Issue, Severity
from resumeforgelint.render.renderer import (
    render,
    _score_to_visual_rating,
    _severity_to_icon,
    _transform_issues,
    _transform_summary,
    _transform_section,
)


class TestScoreToVisualRating:
    def test_positive_good_at_80(self):
        """POSITIVE: score of 80 returns green Good."""
        assert _score_to_visual_rating(80) == ("🟢", "Good")

    def test_positive_good_at_100(self):
        """POSITIVE: perfect score returns green Good."""
        assert _score_to_visual_rating(100) == ("🟢", "Good")

    def test_positive_needs_work_at_50(self):
        """POSITIVE: score of 50 returns yellow Needs Work."""
        assert _score_to_visual_rating(50) == ("🟡", "Needs Work")

    def test_positive_needs_work_at_79(self):
        """POSITIVE: score of 79 returns yellow Needs Work."""
        assert _score_to_visual_rating(79) == ("🟡", "Needs Work")

    def test_positive_poor_at_49(self):
        """POSITIVE: score of 49 returns red Poor."""
        assert _score_to_visual_rating(49) == ("🔴", "Poor")

    def test_positive_poor_at_0(self):
        """POSITIVE: score of 0 returns red Poor."""
        assert _score_to_visual_rating(0) == ("🔴", "Poor")


class TestSeverityToIcon:
    def test_positive_critical(self):
        """POSITIVE: CRITICAL returns ✖."""
        assert _severity_to_icon(Severity.CRITICAL) == "✖"

    def test_positive_warning(self):
        """POSITIVE: WARNING returns ⚠."""
        assert _severity_to_icon(Severity.WARNING) == "⚠"

    def test_positive_info(self):
        """POSITIVE: INFO returns i."""
        assert _severity_to_icon(Severity.INFO) == "i"


class TestTransformIssues:
    def test_positive_single_critical_issue(self):
        """POSITIVE: single critical issue renders with ✖ icon."""
        issues = [Issue(Severity.CRITICAL, "missing name")]
        assert _transform_issues(issues) == "✖ missing name"

    def test_positive_sorts_by_severity(self):
        """POSITIVE: issues sorted by severity, critical first."""
        issues = [
            Issue(Severity.INFO, "minor thing"),
            Issue(Severity.CRITICAL, "big problem"),
            Issue(Severity.WARNING, "watch out"),
        ]
        result = _transform_issues(issues, limit=3)
        assert result == "✖ big problem, ⚠ watch out, i minor thing"

    def test_positive_limit_returns_top_n(self):
        """POSITIVE: limit=1 returns only the most severe issue."""
        issues = [
            Issue(Severity.WARNING, "second"),
            Issue(Severity.CRITICAL, "first"),
        ]
        assert _transform_issues(issues, limit=1) == "✖ first"

    def test_positive_empty_issues(self):
        """POSITIVE: empty issues list returns empty string."""
        assert _transform_issues([]) == ""

    def test_negative_limit_zero(self):
        """NEGATIVE: limit=0 returns empty string."""
        issues = [Issue(Severity.CRITICAL, "problem")]
        assert _transform_issues(issues, limit=0) == ""


class TestTransformSummary:
    def test_positive_good_score(self):
        """POSITIVE: high total produces Good rating props."""
        sections = [
            _make_scored_section("Experience", 18),
            _make_scored_section("Skills", 20),
            _make_scored_section("Education", 18),
            _make_scored_section("Summary", 16),
            _make_scored_section("References", 16),
        ]
        result = _transform_summary(sections)
        assert result == {"emoji": "🟢", "rating": "Good", "total": "88"}

    def test_positive_poor_score(self):
        """POSITIVE: low total produces Poor rating props."""
        sections = [
            _make_scored_section("Experience", 5),
            _make_scored_section("Skills", 5),
            _make_scored_section("Education", 5),
            _make_scored_section("Summary", 5),
            _make_scored_section("References", 5),
        ]
        result = _transform_summary(sections)
        assert result == {"emoji": "🔴", "rating": "Poor", "total": "25"}


class TestTransformSection:
    def test_positive_section_with_issues(self):
        """POSITIVE: section with issues includes top issue text."""
        scored = _make_scored_section("Work Experience", 14, [Issue(Severity.WARNING, "missing dates")])
        result = _transform_section(scored)
        assert result["name"] == "Work Experience"
        assert result["emoji"] == "🟡"
        assert result["score"] == 14
        assert "⚠ missing dates" in result["issues"]

    def test_positive_section_no_issues(self):
        """POSITIVE: section with no issues has empty issues string."""
        scored = _make_scored_section("Skills", 20)
        result = _transform_section(scored)
        assert result["issues"] == ""

    def test_positive_header_section_uses_fallback_name(self):
        """POSITIVE: header section with None heading uses 'Header' as name."""
        section = Section(SectionType.HEADER, None, ["John Smith"])
        scored = ScoredSection(section, 20, [])
        result = _transform_section(scored)
        assert result["name"] == "Header"


class TestRenderE2E:
    def test_positive_full_render_output(self):
        """POSITIVE: full e2e render produces exact expected multi-line output."""
        expected = (
            "Overall: 🟡 Needs Work (62/100)\n"
            "\n"
            "  Skills             🟢  18/20  \n"
            "  Work Experience    🟡  14/20  ⚠ missing quantified achievements\n"
            "  Education          🟢  16/20  \n"
            "  Summary            🔴   6/20  ✖ too short, no keywords\n"
            "  Header             🔴   8/20  ✖ missing contact info"
        )
        scored_sections = [
            _make_scored_section("Skills", 18),
            _make_scored_section("Work Experience", 14, [Issue(Severity.WARNING, "missing quantified achievements")]),
            _make_scored_section("Education", 16),
            _make_scored_section("Summary", 6, [Issue(Severity.CRITICAL, "too short, no keywords")]),
            _make_scored_section(None, 8, [Issue(Severity.CRITICAL, "missing contact info")]),
        ]
        result = render(scored_sections)
        assert result == expected


# --- helpers ---

def _make_scored_section(heading: str | None, score: int, issues: list[Issue] | None = None) -> ScoredSection:
    if heading is None:
        section_type = SectionType.HEADER
    else:
        section_type = SectionType.UNKNOWN
        for st in SectionType:
            if st.value in heading.lower():
                section_type = st
                break
    return ScoredSection(
        Section(section_type, heading, ["content"]),
        score,
        issues or [],
    )
