from resumeforgelint.models import Section, SectionType, ScoredSection, ScoringRubric, Issue, Severity
from resumeforgelint.scorer.scorer import score


def _make_section(content: list[str]) -> Section:
    return Section(section_type=SectionType.HEADER, heading=None, content=content)


def _always_pass(section: Section) -> bool:
    return True


def _always_fail(section: Section) -> bool:
    return False


_TEST_RUBRICS = [
    ScoringRubric(title="PassRubric", severity=Severity.INFO, scorer=_always_pass, message="passes", points=5),
    ScoringRubric(title="FailRubric", severity=Severity.CRITICAL, scorer=_always_fail, message="fails always", points=10),
]


class TestScore:
    def test_positive_all_rubrics_pass(self):
        """POSITIVE: when all rubrics pass, full score and no issues."""
        rubrics = [
            ScoringRubric(title="A", severity=Severity.INFO, scorer=_always_pass, message="a", points=5),
            ScoringRubric(title="B", severity=Severity.WARNING, scorer=_always_pass, message="b", points=5),
        ]
        section = _make_section(["content"])
        result = score(section, rubrics)
        assert result.score == 20
        assert result.issues == []

    def test_negative_failing_rubric_deducts_points(self):
        """NEGATIVE: a failing rubric deducts its points and adds an issue."""
        section = _make_section(["content"])
        result = score(section, _TEST_RUBRICS)
        assert result.score == 10
        assert len(result.issues) == 1
        assert result.issues[0].severity == Severity.CRITICAL
        assert result.issues[0].message == "fails always"

    def test_negative_multiple_failures_deduct_cumulatively(self):
        """NEGATIVE: multiple failing rubrics deduct cumulatively."""
        rubrics = [
            ScoringRubric(title="A", severity=Severity.CRITICAL, scorer=_always_fail, message="a fails", points=8),
            ScoringRubric(title="B", severity=Severity.WARNING, scorer=_always_fail, message="b fails", points=7),
        ]
        section = _make_section(["content"])
        result = score(section, rubrics)
        assert result.score == 5
        assert len(result.issues) == 2

    def test_negative_score_clamps_to_zero(self):
        """NEGATIVE: score never goes below 0."""
        rubrics = [
            ScoringRubric(title="Big", severity=Severity.CRITICAL, scorer=_always_fail, message="big", points=25),
        ]
        section = _make_section(["content"])
        result = score(section, rubrics)
        assert result.score == 0

    def test_positive_section_preserved(self):
        """POSITIVE: the original section is preserved in the result."""
        section = _make_section(["content"])
        result = score(section, [])
        assert result.section is section

    def test_positive_empty_rubrics_full_score(self):
        """POSITIVE: no rubrics means full score and no issues."""
        section = _make_section(["content"])
        result = score(section, [])
        assert result.score == 20
        assert result.issues == []

    def test_negative_issue_severity_matches_rubric(self):
        """NEGATIVE: issue severity matches the rubric's severity."""
        rubrics = [
            ScoringRubric(title="W", severity=Severity.WARNING, scorer=_always_fail, message="warn", points=3),
        ]
        section = _make_section(["content"])
        result = score(section, rubrics)
        assert result.issues[0].severity == Severity.WARNING
