from resumeforgelint.models import Section, SectionType
from resumeforgelint.scorer.work_experience_rubrics import (
    _section_present,
    _has_quantified_achievements,
    _has_action_verbs,
    _has_date_ranges,
    _has_company_and_role,
)

def _make_experience(content: list[str]) -> Section:
    return Section(section_type=SectionType.EXPERIENCE, heading="Experience", content=content)

class TestSectionPresent:
    def test_positive_has_content(self):
        """POSITIVE: section with content passes."""
        section = _make_experience(["Amazon - SDE", "2020 - Present"])
        assert _section_present(section) is True

    def test_negative_empty_content(self):
        """NEGATIVE: empty section fails."""
        section = _make_experience([])
        assert _section_present(section) is False


class TestHasQuantifiedAchievements:
    def test_positive_percentage(self):
        """POSITIVE: percentage metric is detected."""
        section = _make_experience(["Improved latency by 50%"])
        assert _has_quantified_achievements(section) is True

    def test_positive_dollar_amount(self):
        """POSITIVE: dollar amount is detected."""
        section = _make_experience(["Saved $1.2M in infrastructure costs"])
        assert _has_quantified_achievements(section) is True

    def test_positive_multiplier(self):
        """POSITIVE: multiplier (3x) is detected."""
        section = _make_experience(["Scaled throughput 3x"])
        assert _has_quantified_achievements(section) is True

    def test_positive_large_number(self):
        """POSITIVE: large number is detected."""
        section = _make_experience(["Served 100 million requests daily"])
        assert _has_quantified_achievements(section) is True

    def test_negative_no_numbers(self):
        """NEGATIVE: text without numbers fails."""
        section = _make_experience(["Improved system performance", "Led team meetings"])
        assert _has_quantified_achievements(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_experience([])
        assert _has_quantified_achievements(section) is False


class TestHasActionVerbs:
    def test_positive_built(self):
        """POSITIVE: 'Built' at start of bullet is detected."""
        section = _make_experience(["Built a distributed caching layer"])
        assert _has_action_verbs(section) is True

    def test_positive_with_bullet_marker(self):
        """POSITIVE: action verb after bullet marker is detected."""
        section = _make_experience(["• Delivered new authentication service"])
        assert _has_action_verbs(section) is True

    def test_positive_with_dash_marker(self):
        """POSITIVE: action verb after dash marker is detected."""
        section = _make_experience(["- Implemented CI/CD pipeline"])
        assert _has_action_verbs(section) is True

    def test_positive_case_insensitive(self):
        """POSITIVE: action verb in any case is detected."""
        section = _make_experience(["MANAGED a team of 5 engineers"])
        assert _has_action_verbs(section) is True

    def test_negative_no_action_verbs(self):
        """NEGATIVE: lines without action verbs fail."""
        section = _make_experience(["Responsible for backend systems", "Team player"])
        assert _has_action_verbs(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_experience([])
        assert _has_action_verbs(section) is False


class TestHasDateRanges:
    def test_positive_year_dash_year(self):
        """POSITIVE: '2020 - 2024' date range is detected."""
        section = _make_experience(["Amazon - SDE", "2020 - 2024"])
        assert _has_date_ranges(section) is True

    def test_positive_year_dash_present(self):
        """POSITIVE: '2020 - Present' is detected."""
        section = _make_experience(["2020 - Present"])
        assert _has_date_ranges(section) is True

    def test_positive_month_year_range(self):
        """POSITIVE: 'Jan 2020 - Dec 2023' is detected."""
        section = _make_experience(["Jan 2020 - Dec 2023"])
        assert _has_date_ranges(section) is True

    def test_positive_en_dash(self):
        """POSITIVE: en-dash separator is detected."""
        section = _make_experience(["2020\u20132024"])
        assert _has_date_ranges(section) is True

    def test_negative_no_dates(self):
        """NEGATIVE: text without date ranges fails."""
        section = _make_experience(["Amazon - SDE", "Built things"])
        assert _has_date_ranges(section) is False

    def test_negative_single_year(self):
        """NEGATIVE: single year without range fails."""
        section = _make_experience(["Graduated 2020"])
        assert _has_date_ranges(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_experience([])
        assert _has_date_ranges(section) is False


class TestHasCompanyAndRole:
    def test_positive_dash_separator(self):
        """POSITIVE: 'Company - Role' pattern is detected."""
        section = _make_experience(["Amazon - Senior Software Engineer"])
        assert _has_company_and_role(section) is True

    def test_positive_en_dash_separator(self):
        """POSITIVE: en-dash separator is detected."""
        section = _make_experience(["Google \u2013 Staff Engineer"])
        assert _has_company_and_role(section) is True

    def test_positive_at_pattern(self):
        """POSITIVE: 'Role at Company' pattern is detected."""
        section = _make_experience(["Senior Engineer at Amazon"])
        assert _has_company_and_role(section) is True

    def test_negative_no_separator(self):
        """NEGATIVE: line without dash or 'at' fails."""
        section = _make_experience(["Built distributed systems", "Led team"])
        assert _has_company_and_role(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_experience([])
        assert _has_company_and_role(section) is False
