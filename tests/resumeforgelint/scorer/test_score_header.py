import pytest

from resumeforgelint.models import Section, SectionType, Severity
from resumeforgelint.scorer.score_header import score_header, _contains_full_name_at_start


def _make_header(content: list[str]) -> Section:
    return Section(section_type=SectionType.HEADER, heading=None, content=content)


class TestContainsFullNameAtStart:
    def test_positive_two_word_name(self):
        """POSITIVE: two-word capitalized name alone on first line is detected."""
        section = _make_header(["John Smith", "john@email.com"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_whitespace_trimmed(self):
        """POSITIVE: leading/trailing whitespace is ignored."""
        section = _make_header(["  John Smith  ", "john@email.com"])
        assert _contains_full_name_at_start(section) is True

    def test_negative_empty_content(self):
        """NEGATIVE: empty content returns False."""
        section = _make_header([])
        assert _contains_full_name_at_start(section) is False

    def test_negative_no_name(self):
        """NEGATIVE: first line without a name returns False."""
        section = _make_header(["john@email.com", "555-1234"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_lowercase_name(self):
        """NEGATIVE: lowercase name is not detected."""
        section = _make_header(["john smith", "john@email.com"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_name_with_prefix(self):
        """NEGATIVE: name with a prefix on the line fails."""
        section = _make_header(["Name: John Smith"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_name_with_suffix(self):
        """NEGATIVE: name with trailing text on the line fails."""
        section = _make_header(["John Smith | Engineer"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_three_word_name(self):
        """NEGATIVE: three-word name does not match two-word pattern (known limitation)."""
        section = _make_header(["Mary Jane Watson"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_hyphenated_name(self):
        """NEGATIVE: hyphenated name is not detected (known limitation)."""
        section = _make_header(["Mary-Jane Watson"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_apostrophe_name(self):
        """NEGATIVE: apostrophe in surname is not detected (known limitation)."""
        section = _make_header(["Patrick O'Brien"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_single_name(self):
        """NEGATIVE: single word name is not detected."""
        section = _make_header(["Madonna"])
        assert _contains_full_name_at_start(section) is False


class TestScoreHeader:
    def test_positive_valid_header_full_score(self):
        """POSITIVE: header with valid name gets full 20 points and no issues."""
        section = _make_header(["John Smith", "john@email.com", "555-1234"])
        result = score_header(section)
        assert result.score == 20
        assert result.issues == []

    def test_negative_no_name_deducts_points_with_message(self):
        """NEGATIVE: header without a name deducts 10 points and reports critical issue with message."""
        section = _make_header(["john@email.com", "555-1234"])
        result = score_header(section)
        assert result.score == 10
        assert len(result.issues) == 1
        assert result.issues[0].severity == Severity.CRITICAL
        assert "full name" in result.issues[0].message.lower()

    def test_negative_empty_header_reports_issue(self):
        """NEGATIVE: empty header section deducts points and reports issue."""
        section = _make_header([])
        result = score_header(section)
        assert result.score == 10
        assert len(result.issues) == 1
        assert result.issues[0].severity == Severity.CRITICAL
        assert "full name" in result.issues[0].message.lower()

    def test_positive_section_preserved_in_result(self):
        """POSITIVE: original section is preserved in the scored result."""
        section = _make_header(["Jane Doe", "jane@test.com"])
        result = score_header(section)
        assert result.section is section
