import pytest

from resumeforgelint.render.template_engine import TemplateEngine


class TestTemplateEngine:
    def test_positive_exact_output_matches_expected(self):
        """POSITIVE: full render matches the exact expected multi-line output."""
        expected = (
            "Overall: 🟡 Needs Work (62/100)\n"
            "\n"
            "  Skills             🟢  18/20  \n"
            "  Work Experience    🟡  14/20  ⚠ missing quantified achievements\n"
            "  Education          🟢  16/20  \n"
            "  Summary            🔴   6/20  ✖ too short, no keywords\n"
            "  References         —   0/20  not found (optional)"
        )
        result = (
            TemplateEngine()
            .summary({"emoji": "🟡", "rating": "Needs Work", "total": "62"})
            .section({"name": "Skills", "emoji": "🟢", "score": 18, "issue": ""})
            .section({"name": "Work Experience", "emoji": "🟡", "score": 14, "issue": "⚠ missing quantified achievements"})
            .section({"name": "Education", "emoji": "🟢", "score": 16, "issue": ""})
            .section({"name": "Summary", "emoji": "🔴", "score": 6, "issue": "✖ too short, no keywords"})
            .section({"name": "References", "emoji": "—", "score": 0, "issue": "not found (optional)"})
            .render()
        )
        assert result == expected

    def test_positive_full_render(self):
        """POSITIVE: renders complete report with summary and sections."""
        template = TemplateEngine()
        result = (
            template
            .summary({"emoji": "🟡", "rating": "Needs Work", "total": "62"})
            .section({"name": "Skills", "emoji": "🟢", "score": 18, "issue": ""})
            .section({"name": "Work Experience", "emoji": "🟡", "score": 14, "issue": "⚠ missing quantified achievements"})
            .render()
        )
        assert "Overall: 🟡 Needs Work (62/100)" in result
        assert "Skills" in result
        assert "Work Experience" in result
        assert "⚠ missing quantified achievements" in result

    def test_positive_summary_and_sections_separated_by_blank_line(self):
        """POSITIVE: summary and sections are separated by a blank line."""
        template = TemplateEngine()
        result = (
            template
            .summary({"emoji": "🟢", "rating": "Good", "total": "85"})
            .section({"name": "Skills", "emoji": "🟢", "score": 20, "issue": ""})
            .render()
        )
        assert "\n\n" in result

    def test_positive_multiple_sections_on_separate_lines(self):
        """POSITIVE: each section appears on its own line."""
        template = TemplateEngine()
        result = (
            template
            .summary({"emoji": "🟢", "rating": "Good", "total": "80"})
            .section({"name": "Skills", "emoji": "🟢", "score": 20, "issue": ""})
            .section({"name": "Education", "emoji": "🟢", "score": 20, "issue": ""})
            .section({"name": "Experience", "emoji": "🟢", "score": 20, "issue": ""})
            .render()
        )
        lines = result.split("\n")
        section_lines = [l for l in lines if l.strip().startswith(("Skills", "Education", "Experience"))]
        assert len(section_lines) == 3

    def test_positive_extra_props_silently_ignored(self):
        """POSITIVE: extra keys in props dict not in template are silently ignored."""
        template = TemplateEngine()
        result = (
            template
            .summary({"emoji": "🟢", "rating": "Good", "total": "80", "extra_key": "ignored"})
            .section({"name": "Skills", "emoji": "🟢", "score": 20, "issue": "", "unused": "value"})
            .render()
        )
        assert "Overall: 🟢 Good (80/100)" in result
        assert "ignored" not in result
        assert "value" not in result

    def test_positive_chaining_returns_self(self):
        """POSITIVE: summary() and section() return self for method chaining."""
        template = TemplateEngine()
        assert template.summary({"emoji": "🟢", "rating": "Good", "total": "80"}) is template
        assert template.section({"name": "Skills", "emoji": "🟢", "score": 20, "issue": ""}) is template

    def test_negative_render_without_summary_raises(self):
        """NEGATIVE: render without calling summary() raises ValueError."""
        template = TemplateEngine()
        template.section({"name": "Skills", "emoji": "🟢", "score": 20, "issue": ""})
        with pytest.raises(ValueError, match="SUMMARY"):
            template.render()

    def test_negative_render_without_sections_raises(self):
        """NEGATIVE: render without any section() calls raises ValueError."""
        template = TemplateEngine()
        template.summary({"emoji": "🟢", "rating": "Good", "total": "80"})
        with pytest.raises(ValueError, match="SECTION"):
            template.render()

    def test_negative_render_empty_template_raises(self):
        """NEGATIVE: render on fresh template raises ValueError."""
        template = TemplateEngine()
        with pytest.raises(ValueError):
            template.render()

    def test_negative_missing_summary_prop_raises(self):
        """NEGATIVE: missing required key in summary props raises KeyError with key name."""
        template = TemplateEngine()
        with pytest.raises(KeyError, match="total"):
            template.summary({"emoji": "🟢", "rating": "Good"})  # missing 'total'

    def test_negative_missing_section_prop_raises(self):
        """NEGATIVE: missing required key in section props raises KeyError with key name."""
        template = TemplateEngine()
        with pytest.raises(KeyError, match="score"):
            template.section({"name": "Skills", "emoji": "🟢", "issue": ""})  # missing 'score'
