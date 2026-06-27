from resumeforgelint.models import Section, SectionType
from resumeforgelint.scorer.education_rubrics import (
    _section_present,
    _has_degree_type,
    _has_institution,
    _has_graduation_date,
)


def _make_education(content: list[str]) -> Section:
    return Section(section_type=SectionType.EDUCATION, heading="Education", content=content)


class TestSectionPresent:
    def test_positive_has_content(self):
        """POSITIVE: section with content passes."""
        section = _make_education(["BSc Computer Science, University of Edinburgh, 2016"])
        assert _section_present(section) is True

    def test_negative_empty_content(self):
        """NEGATIVE: empty section fails."""
        section = _make_education([])
        assert _section_present(section) is False


class TestHasDegreeType:
    def test_positive_bsc(self):
        """POSITIVE: BSc is detected."""
        section = _make_education(["BSc Computer Science"])
        assert _has_degree_type(section) is True

    def test_positive_msc(self):
        """POSITIVE: MSc is detected."""
        section = _make_education(["MSc Data Science"])
        assert _has_degree_type(section) is True

    def test_positive_phd(self):
        """POSITIVE: PhD is detected."""
        section = _make_education(["PhD in Machine Learning"])
        assert _has_degree_type(section) is True

    def test_positive_bachelor(self):
        """POSITIVE: 'Bachelor' word is detected."""
        section = _make_education(["Bachelor of Arts in English"])
        assert _has_degree_type(section) is True

    def test_positive_master(self):
        """POSITIVE: 'Master' word is detected."""
        section = _make_education(["Master of Business Administration"])
        assert _has_degree_type(section) is True

    def test_positive_mba(self):
        """POSITIVE: MBA is detected."""
        section = _make_education(["MBA, Harvard Business School"])
        assert _has_degree_type(section) is True

    def test_positive_with_dots(self):
        """POSITIVE: B.Sc with dots is detected."""
        section = _make_education(["B.Sc. Computer Science"])
        assert _has_degree_type(section) is True

    def test_negative_no_degree(self):
        """NEGATIVE: no degree type fails."""
        section = _make_education(["University of Edinburgh, 2016"])
        assert _has_degree_type(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_education([])
        assert _has_degree_type(section) is False


class TestHasInstitution:
    def test_positive_university(self):
        """POSITIVE: 'University' is detected."""
        section = _make_education(["BSc, University of Edinburgh"])
        assert _has_institution(section) is True

    def test_positive_college(self):
        """POSITIVE: 'College' is detected."""
        section = _make_education(["Imperial College London"])
        assert _has_institution(section) is True

    def test_positive_institute(self):
        """POSITIVE: 'Institute' is detected."""
        section = _make_education(["Massachusetts Institute of Technology"])
        assert _has_institution(section) is True

    def test_positive_school(self):
        """POSITIVE: 'School' is detected."""
        section = _make_education(["London School of Economics"])
        assert _has_institution(section) is True

    def test_negative_no_institution(self):
        """NEGATIVE: no institution keyword fails."""
        section = _make_education(["BSc Computer Science, 2016"])
        assert _has_institution(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_education([])
        assert _has_institution(section) is False


class TestHasGraduationDate:
    def test_positive_four_digit_year(self):
        """POSITIVE: 4-digit year is detected."""
        section = _make_education(["BSc Computer Science, 2016"])
        assert _has_graduation_date(section) is True

    def test_positive_recent_year(self):
        """POSITIVE: recent year is detected."""
        section = _make_education(["MSc, University of Oxford, 2023"])
        assert _has_graduation_date(section) is True

    def test_negative_no_year(self):
        """NEGATIVE: no year fails."""
        section = _make_education(["BSc Computer Science, University of Edinburgh"])
        assert _has_graduation_date(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content fails."""
        section = _make_education([])
        assert _has_graduation_date(section) is False
