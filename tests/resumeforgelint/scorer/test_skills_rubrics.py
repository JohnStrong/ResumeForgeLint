from resumeforgelint.models import Section, SectionType
from resumeforgelint.scorer.skills_rubrics import (
    _section_present,
    _contains_technical_keywords,
    _meets_minimum_keyword_count,
    _no_excessive_soft_skill_filler,
)


def _make_skills(content: list[str]) -> Section:
    return Section(section_type=SectionType.SKILLS, heading="Skills", content=content)


class TestSectionPresent:
    def test_positive_has_content(self):
        """POSITIVE: section with content passes."""
        section = _make_skills(["Python, Java, AWS"])
        assert _section_present(section) is True

    def test_negative_empty_content(self):
        """NEGATIVE: empty section fails."""
        section = _make_skills([])
        assert _section_present(section) is False


class TestContainsTechnicalKeywords:
    def test_positive_programming_language(self):
        """POSITIVE: programming language is detected."""
        section = _make_skills(["Python, Java"])
        assert _contains_technical_keywords(section) is True

    def test_positive_cloud_platform(self):
        """POSITIVE: cloud platform is detected."""
        section = _make_skills(["AWS, Azure, GCP"])
        assert _contains_technical_keywords(section) is True

    def test_positive_tool(self):
        """POSITIVE: tool/framework is detected."""
        section = _make_skills(["Docker, Kubernetes, Terraform"])
        assert _contains_technical_keywords(section) is True

    def test_positive_database(self):
        """POSITIVE: database technology is detected."""
        section = _make_skills(["PostgreSQL, MongoDB, Redis"])
        assert _contains_technical_keywords(section) is True

    def test_positive_bullet_points(self):
        """POSITIVE: keywords in bullet point format are detected."""
        section = _make_skills(["• Python", "• Java", "• AWS"])
        assert _contains_technical_keywords(section) is True

    def test_positive_dash_list(self):
        """POSITIVE: keywords in dash-delimited list are detected."""
        section = _make_skills(["- Python", "- Docker", "- Kubernetes"])
        assert _contains_technical_keywords(section) is True

    def test_positive_semicolon_delimited(self):
        """POSITIVE: keywords separated by semicolons are detected."""
        section = _make_skills(["Python; Java; AWS; Docker; Git"])
        assert _contains_technical_keywords(section) is True

    def test_positive_numbered_list(self):
        """POSITIVE: keywords in numbered list are detected."""
        section = _make_skills(["1. Python", "2. Java", "3. AWS"])
        assert _contains_technical_keywords(section) is True

    def test_positive_em_dash_delimited(self):
        """POSITIVE: keywords with em-dash separators are detected."""
        section = _make_skills(["Python — Java — AWS"])
        assert _contains_technical_keywords(section) is True

    def test_negative_no_technical_terms(self):
        """NEGATIVE: no technical keywords fails."""
        section = _make_skills(["Communication, Leadership, Teamwork"])
        assert _contains_technical_keywords(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_skills([])
        assert _contains_technical_keywords(section) is False


class TestMeetsMinimumKeywordCount:
    def test_positive_meets_threshold(self):
        """POSITIVE: 5+ keywords passes."""
        section = _make_skills(["Python, Java, AWS, Docker, Kubernetes, Git"])
        assert _meets_minimum_keyword_count(section) is True

    def test_positive_across_multiple_lines(self):
        """POSITIVE: keywords across multiple lines are counted."""
        section = _make_skills(["Python, Java, AWS", "Docker, Kubernetes"])
        assert _meets_minimum_keyword_count(section) is True

    def test_negative_below_threshold(self):
        """NEGATIVE: fewer than 5 keywords fails."""
        section = _make_skills(["Python, Java"])
        assert _meets_minimum_keyword_count(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_skills([])
        assert _meets_minimum_keyword_count(section) is False


class TestNoExcessiveSoftSkillFiller:
    def test_positive_no_filler(self):
        """POSITIVE: technical-only content passes."""
        section = _make_skills(["Python, Java, AWS, Docker"])
        assert _no_excessive_soft_skill_filler(section) is True

    def test_negative_team_player(self):
        """NEGATIVE: 'team player' filler detected."""
        section = _make_skills(["Python, Java", "Team player, Hard worker"])
        assert _no_excessive_soft_skill_filler(section) is False

    def test_negative_self_starter(self):
        """NEGATIVE: 'self-starter' filler detected."""
        section = _make_skills(["Self-starter with Python experience"])
        assert _no_excessive_soft_skill_filler(section) is False

    def test_negative_motivated(self):
        """NEGATIVE: 'motivated' filler detected."""
        section = _make_skills(["Motivated developer with AWS skills"])
        assert _no_excessive_soft_skill_filler(section) is False

    def test_positive_empty_content(self):
        """POSITIVE: empty content has no filler (passes)."""
        section = _make_skills([])
        assert _no_excessive_soft_skill_filler(section) is True
