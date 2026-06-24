import pytest

from resumeforgelint.models import Section, SectionType
from resumeforgelint.parser.section_parser import parse, _match_heading


class TestMatchHeading:
    def test_positive_exact_match(self):
        """POSITIVE: exact synonym matches return correct SectionType."""
        assert _match_heading("Experience") == SectionType.EXPERIENCE
        assert _match_heading("Skills") == SectionType.SKILLS
        assert _match_heading("Education") == SectionType.EDUCATION
        assert _match_heading("Summary") == SectionType.SUMMARY
        assert _match_heading("References") == SectionType.REFERENCES

    def test_positive_case_insensitive(self):
        """POSITIVE: headings match regardless of case."""
        assert _match_heading("EXPERIENCE") == SectionType.EXPERIENCE
        assert _match_heading("skills") == SectionType.SKILLS
        assert _match_heading("EDUCATION") == SectionType.EDUCATION

    def test_positive_synonym_variants(self):
        """POSITIVE: synonym variants resolve to canonical section type."""
        assert _match_heading("Work Experience") == SectionType.EXPERIENCE
        assert _match_heading("Work History") == SectionType.EXPERIENCE
        assert _match_heading("Employment") == SectionType.EXPERIENCE
        assert _match_heading("Professional Experience") == SectionType.EXPERIENCE
        assert _match_heading("Profile") == SectionType.SUMMARY
        assert _match_heading("Objective") == SectionType.SUMMARY
        assert _match_heading("About Me") == SectionType.SUMMARY
        assert _match_heading("Academics") == SectionType.EDUCATION
        assert _match_heading("Qualifications") == SectionType.EDUCATION
        assert _match_heading("Technical Skills") == SectionType.SKILLS
        assert _match_heading("Core Competencies") == SectionType.SKILLS
        assert _match_heading("Competencies") == SectionType.SKILLS

    def test_positive_whitespace_stripped(self):
        """POSITIVE: leading/trailing whitespace is ignored."""
        assert _match_heading("  Skills  ") == SectionType.SKILLS
        assert _match_heading("\tEducation\t") == SectionType.EDUCATION

    def test_negative_unrecognized_heading(self):
        """NEGATIVE: non-section text returns None."""
        assert _match_heading("Projects") is None
        assert _match_heading("Volunteer Work") is None
        assert _match_heading("Certifications") is None

    def test_negative_partial_match(self):
        """NEGATIVE: partial matches do not resolve (no substring matching)."""
        assert _match_heading("My Skills Section") is None
        assert _match_heading("Work Experience at Amazon") is None

    def test_negative_empty_line(self):
        """NEGATIVE: empty or blank lines return None."""
        assert _match_heading("") is None
        assert _match_heading("   ") is None


class TestParse:
    def test_positive_full_resume(self):
        """POSITIVE: parses a complete resume into all expected sections."""
        text = (
            "John Doe\njohn@email.com\n\n"
            "Summary\nExperienced developer.\n\n"
            "Experience\nAmazon - SDE\n2020-2024\n\n"
            "Education\nBSc Computer Science\n\n"
            "Skills\nPython, AWS\n\n"
            "References\nAvailable on request"
        )
        sections = parse(text)

        assert len(sections) == 6
        assert sections[0].section_type == SectionType.HEADER
        assert sections[0].heading is None
        assert "John Doe" in sections[0].content

        assert sections[1].section_type == SectionType.SUMMARY
        assert sections[1].heading == "Summary"

        assert sections[2].section_type == SectionType.EXPERIENCE
        assert sections[2].heading == "Experience"

        assert sections[3].section_type == SectionType.EDUCATION
        assert sections[3].heading == "Education"

        assert sections[4].section_type == SectionType.SKILLS
        assert sections[4].heading == "Skills"

        assert sections[5].section_type == SectionType.REFERENCES
        assert sections[5].heading == "References"

    def test_positive_header_before_first_section(self):
        """POSITIVE: content before first recognized heading becomes the header section."""
        text = "Jane Smith\njanee@test.com\n555-1234\n\nSkills\nPython"
        sections = parse(text)

        assert sections[0].section_type == SectionType.HEADER
        assert sections[0].heading is None
        assert "Jane Smith" in sections[0].content
        assert "555-1234" in sections[0].content

    def test_positive_section_content_captured(self):
        """POSITIVE: all lines between headings are captured as content."""
        text = "Name\n\nExperience\nLine 1\nLine 2\nLine 3\n\nSkills\nPython"
        sections = parse(text)

        exp_section = next(s for s in sections if s.section_type == SectionType.EXPERIENCE)
        assert "Line 1" in exp_section.content
        assert "Line 2" in exp_section.content
        assert "Line 3" in exp_section.content

    def test_positive_synonym_heading_preserved(self):
        """POSITIVE: original heading text is preserved even when synonym resolves type."""
        text = "Name\n\nWork History\nDid things"
        sections = parse(text)

        exp_section = next(s for s in sections if s.section_type == SectionType.EXPERIENCE)
        assert exp_section.heading == "Work History"

    def test_positive_empty_section_content(self):
        """POSITIVE: a heading immediately followed by another heading produces empty content."""
        text = "Name\n\nSkills\nEducation\nBSc"
        sections = parse(text)

        skills_section = next(s for s in sections if s.section_type == SectionType.SKILLS)
        assert skills_section.content == []

    def test_negative_empty_string_raises(self):
        """NEGATIVE: empty string raises ValueError."""
        with pytest.raises(ValueError, match="Cannot score an empty Resume"):
            parse("")

    def test_negative_none_raises(self):
        """NEGATIVE: None input raises ValueError."""
        with pytest.raises((ValueError, TypeError)):
            parse(None)

    def test_negative_no_recognized_sections(self):
        """NEGATIVE: text with no recognized headings returns only the header section."""
        text = "John Doe\njohn@email.com\nSome random content"
        sections = parse(text)

        assert len(sections) == 1
        assert sections[0].section_type == SectionType.HEADER
        assert sections[0].heading is None

    def test_negative_heading_embedded_in_sentence(self):
        """NEGATIVE: heading keywords inside sentences are not matched as boundaries."""
        text = "Name\n\nExperience\nI have experience in skills development"
        sections = parse(text)

        # "skills development" should NOT create a new Skills section
        assert not any(
            s.section_type == SectionType.SKILLS for s in sections
        )
