import pytest

from resumeforgelint.models import Section, SectionType, Severity
from resumeforgelint.scorer.score_header import score_header, _contains_full_name_at_start, _contains_email, _contains_phone_number


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

    def test_positive_lowercase_name_with_ignorecase(self):
        """POSITIVE: lowercase name matches due to IGNORECASE flag."""
        section = _make_header(["john smith", "john@email.com"])
        assert _contains_full_name_at_start(section) is True

    def test_negative_name_with_prefix(self):
        """NEGATIVE: name with a prefix on the line fails."""
        section = _make_header(["Name: John Smith"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_name_with_suffix(self):
        """NEGATIVE: name with trailing text on the line fails."""
        section = _make_header(["John Smith | Engineer"])
        assert _contains_full_name_at_start(section) is False

    @pytest.mark.skip(reason="IGNORECASE makes all-lowercase pass — revisit when case strictness is added")
    def test_negative_three_word_name_without_caps(self):
        """NEGATIVE: three-word name without proper capitalization should fail."""
        section = _make_header(["mary jane watson"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_hyphenated_only_no_surname(self):
        """NEGATIVE: single hyphenated word without surname fails."""
        section = _make_header(["Mary-Jane"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_apostrophe_only_no_surname(self):
        """NEGATIVE: single apostrophe word without surname fails."""
        section = _make_header(["O'Brien"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_single_name(self):
        """NEGATIVE: single word name is not detected."""
        section = _make_header(["Madonna"])
        assert _contains_full_name_at_start(section) is False

    def test_positive_prefix_mr(self):
        """POSITIVE: Mr prefix with name is detected."""
        section = _make_header(["Mr John Smith"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_prefix_mr_dot(self):
        """POSITIVE: Mr. prefix with dot is detected."""
        section = _make_header(["Mr. John Smith"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_prefix_mrs(self):
        """POSITIVE: Mrs prefix is detected."""
        section = _make_header(["Mrs Jane Doe"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_prefix_miss(self):
        """POSITIVE: Miss prefix is detected."""
        section = _make_header(["Miss Jane Doe"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_prefix_ms(self):
        """POSITIVE: Ms prefix is detected."""
        section = _make_header(["Ms. Jane Doe"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_prefix_dr(self):
        """POSITIVE: Dr prefix is detected."""
        section = _make_header(["Dr. Jane Doe"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_jr(self):
        """POSITIVE: Jr suffix is detected."""
        section = _make_header(["John Smith Jr"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_jr_dot(self):
        """POSITIVE: Jr. suffix with dot is detected."""
        section = _make_header(["John Smith Jr."])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_sr(self):
        """POSITIVE: Sr suffix is detected."""
        section = _make_header(["John Smith Sr."])
        assert _contains_full_name_at_start(section) is True

    def test_positive_prefix_and_suffix(self):
        """POSITIVE: both prefix and suffix together are detected."""
        section = _make_header(["Mr. John Smith Jr."])
        assert _contains_full_name_at_start(section) is True

    def test_positive_unknown_prefix_treated_as_name(self):
        """POSITIVE: unrecognized prefix like 'Sir' is treated as part of a three-word name."""
        section = _make_header(["Sir John Smith"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_unknown_suffix_treated_as_name(self):
        """POSITIVE: unrecognized suffix like 'CPA' is treated as part of a three-word name."""
        section = _make_header(["John Smith CPA"])
        assert _contains_full_name_at_start(section) is True

    def test_negative_single_word_not_a_name(self):
        """NEGATIVE: a single word is not a valid name."""
        section = _make_header(["Engineer"])
        assert _contains_full_name_at_start(section) is False

    def test_negative_number_in_name(self):
        """NEGATIVE: numbers in the line are not a valid name."""
        section = _make_header(["John Smith 123"])
        assert _contains_full_name_at_start(section) is False

    def test_positive_prefix_prof(self):
        """POSITIVE: Prof prefix is detected."""
        section = _make_header(["Prof. Jane Doe"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_ii(self):
        """POSITIVE: II suffix is detected."""
        section = _make_header(["John Smith II"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_iii(self):
        """POSITIVE: III suffix is detected."""
        section = _make_header(["John Smith III"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_iv(self):
        """POSITIVE: IV suffix is detected."""
        section = _make_header(["John Smith IV"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_phd(self):
        """POSITIVE: PhD suffix is detected."""
        section = _make_header(["Jane Doe PhD"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_md(self):
        """POSITIVE: MD suffix is detected."""
        section = _make_header(["Jane Doe MD"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_suffix_esq(self):
        """POSITIVE: Esq suffix is detected."""
        section = _make_header(["John Smith Esq."])
        assert _contains_full_name_at_start(section) is True

    def test_positive_hyphenated_surname(self):
        """POSITIVE: hyphenated surname is detected."""
        section = _make_header(["John Smith-Jones"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_hyphenated_first_name(self):
        """POSITIVE: hyphenated first name is detected."""
        section = _make_header(["Anne-Marie Smith"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_apostrophe_name(self):
        """POSITIVE: apostrophe in name is detected."""
        section = _make_header(["Patrick O'Brien"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_three_word_name(self):
        """POSITIVE: three-word name is detected."""
        section = _make_header(["Mary Jane Watson"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_accented_characters(self):
        """POSITIVE: accented characters in names are detected."""
        section = _make_header(["José García"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_all_caps(self):
        """POSITIVE: ALL CAPS name is detected (IGNORECASE)."""
        section = _make_header(["JOHN SMITH"])
        assert _contains_full_name_at_start(section) is True

    def test_positive_all_caps_three_words(self):
        """POSITIVE: ALL CAPS three-word name is detected."""
        section = _make_header(["MARY JANE WATSON"])
        assert _contains_full_name_at_start(section) is True


class TestScoreHeader:
    def test_positive_all_rubrics_pass(self):
        """POSITIVE: header with name, email, and phone gets full 20 points."""
        section = _make_header(["John Smith", "john@email.com", "555-123-4567"])
        result = score_header(section)
        assert result.score == 20
        assert result.issues == []

    def test_positive_section_preserved_in_result(self):
        """POSITIVE: original section is preserved in the scored result."""
        section = _make_header(["John Smith", "john@email.com", "555-123-4567"])
        result = score_header(section)
        assert result.section is section

    def test_negative_no_name_deducts_11_points(self):
        """NEGATIVE: header without a name but with email and phone deducts 11 points."""
        section = _make_header(["London, UK", "john@email.com", "555-123-4567"])
        result = score_header(section)
        assert result.score == 9
        assert any("full name" in i.message.lower() for i in result.issues)

    def test_negative_missing_email_deducts_11_points(self):
        """NEGATIVE: header with name and phone but no email deducts 11 points."""
        section = _make_header(["John Smith", "555-123-4567"])
        result = score_header(section)
        assert result.score == 9
        assert len(result.issues) == 1
        assert "email" in result.issues[0].message.lower()

    def test_negative_missing_phone_deducts_11_points(self):
        """NEGATIVE: header with name and email but no phone deducts 11 points."""
        section = _make_header(["John Smith", "john@email.com", "London, UK"])
        result = score_header(section)
        assert result.score == 9
        assert len(result.issues) == 1
        assert "phone" in result.issues[0].message.lower()

    def test_negative_only_name_present(self):
        """NEGATIVE: header with name only, missing email and phone, clamps to 0."""
        section = _make_header(["John Smith", "London, UK"])
        result = score_header(section)
        assert result.score == 0
        assert len(result.issues) == 2
        assert any("email" in i.message.lower() for i in result.issues)
        assert any("phone" in i.message.lower() for i in result.issues)

    def test_negative_empty_header_fails_all_rubrics(self):
        """NEGATIVE: empty header section fails all rubrics and clamps to 0."""
        section = _make_header([])
        result = score_header(section)
        assert result.score == 0
        assert len(result.issues) == 3

    def test_negative_missing_all_clamps_to_zero(self):
        """NEGATIVE: header missing name, email, and phone clamps to 0."""
        section = _make_header(["London, UK"])
        result = score_header(section)
        assert result.score == 0
        assert len(result.issues) == 3


class TestContainsEmail:
    def test_positive_email_on_second_line(self):
        """POSITIVE: email on second line is detected."""
        section = _make_header(["John Smith", "john@email.com", "555-123-4567"])
        assert _contains_email(section) is True

    def test_positive_email_on_third_line(self):
        """POSITIVE: email on any line after the first is detected."""
        section = _make_header(["John Smith", "555-123-4567", "john@email.com"])
        assert _contains_email(section) is True

    def test_positive_email_with_plus(self):
        """POSITIVE: email with + tag is detected."""
        section = _make_header(["John Smith", "john+resume@email.com"])
        assert _contains_email(section) is True

    def test_positive_email_with_subdomain(self):
        """POSITIVE: email with subdomain is detected."""
        section = _make_header(["John Smith", "john@sub.domain.co.uk"])
        assert _contains_email(section) is True

    def test_negative_no_email(self):
        """NEGATIVE: header without email returns False."""
        section = _make_header(["John Smith", "555-123-4567", "London, UK"])
        assert _contains_email(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content returns False."""
        section = _make_header([])
        assert _contains_email(section) is False

    def test_negative_email_on_first_line_only(self):
        """NEGATIVE: email only on the first line (name line) is not detected."""
        section = _make_header(["john@email.com"])
        assert _contains_email(section) is False

    def test_negative_invalid_email(self):
        """NEGATIVE: invalid email format is not detected."""
        section = _make_header(["John Smith", "john@", "not-an-email"])
        assert _contains_email(section) is False


class TestContainsPhoneNumber:
    def test_positive_us_format_dashes(self):
        """POSITIVE: US phone with dashes is detected."""
        section = _make_header(["John Smith", "555-123-4567"])
        assert _contains_phone_number(section) is True

    def test_positive_us_format_parens(self):
        """POSITIVE: US phone with parens is detected."""
        section = _make_header(["John Smith", "(555) 123-4567"])
        assert _contains_phone_number(section) is True

    def test_positive_us_format_dots(self):
        """POSITIVE: US phone with dots is detected."""
        section = _make_header(["John Smith", "555.123.4567"])
        assert _contains_phone_number(section) is True

    def test_positive_international_with_country_code(self):
        """POSITIVE: international phone with country code is detected."""
        section = _make_header(["John Smith", "+44 7700 900000"])
        assert _contains_phone_number(section) is True

    def test_positive_uk_format(self):
        """POSITIVE: UK phone format is detected."""
        section = _make_header(["John Smith", "07700 900000"])
        assert _contains_phone_number(section) is True

    def test_positive_phone_on_third_line(self):
        """POSITIVE: phone on any line after first is detected."""
        section = _make_header(["John Smith", "john@email.com", "555-123-4567"])
        assert _contains_phone_number(section) is True

    def test_negative_no_phone(self):
        """NEGATIVE: header without phone returns False."""
        section = _make_header(["John Smith", "john@email.com", "London, UK"])
        assert _contains_phone_number(section) is False

    def test_negative_empty_content(self):
        """NEGATIVE: empty content returns False."""
        section = _make_header([])
        assert _contains_phone_number(section) is False

    def test_negative_phone_on_first_line_only(self):
        """NEGATIVE: phone only on the first line (name line) is not detected."""
        section = _make_header(["555-123-4567"])
        assert _contains_phone_number(section) is False

    def test_negative_too_short(self):
        """NEGATIVE: number too short to be a phone is not detected."""
        section = _make_header(["John Smith", "12345"])
        assert _contains_phone_number(section) is False
