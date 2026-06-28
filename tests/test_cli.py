import subprocess
from pathlib import Path

import pytest

from resumeforgelint.cli import _validate, _parse_args

EXAMPLES_DIR = Path(__file__).parents[1] / "examples"


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["resumeforgelint", *args],
        capture_output=True,
        text=True,
    )


class TestCli:
    def test_positive_help(self):
        """POSITIVE: --help prints usage and exits 0."""
        result = _run_cli("--help")
        assert result.returncode == 0
        assert "validate" in result.stdout

    def test_positive_validate_good_header(self):
        """POSITIVE: validate with good header and experience produces expected output."""
        expected = (
            "Overall: 🟢 Good (80/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Experience         🟢  20/20  \n"
            "  Education          🟢  20/20  \n"
            "  Skills             🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "good_header.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_bad_header(self):
        """POSITIVE: validate with bad header resume produces expected output."""
        expected = (
            "Overall: 🟡 Needs Work (60/80)\n"
            "\n"
            "  Header             🔴   0/20  ✖ A Resume should contain the applicants full name at the start (top) of the document\n"
            "  Experience         🟢  20/20  \n"
            "  Education          🟢  20/20  \n"
            "  Skills             🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_header.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_negative_no_command(self):
        """NEGATIVE: no command prints help and exits 0."""
        result = _run_cli()
        assert result.returncode == 0
        assert "validate" in result.stdout

    def test_negative_validate_missing_input(self):
        """NEGATIVE: validate without --input exits 2."""
        result = _run_cli("validate")
        assert result.returncode == 2
        assert "--input" in result.stderr

    def test_negative_validate_file_not_found(self):
        """NEGATIVE: validate with non-existent file exits 1."""
        result = _run_cli("validate", "--input", "nonexistent.txt")
        assert result.returncode == 1
        assert "not found" in result.stdout

    def test_positive_validate_bad_experience(self):
        """POSITIVE: validate with bad experience section reports issues."""
        expected = (
            "Overall: 🔴 Poor (20/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Experience         🔴   0/20  ✖ Each role should include company name and role title\n"
            "  Education          🔴   0/20  ✖ Education section should not be empty\n"
            "  Skills             🔴   0/20  ✖ Skills section should not be empty\n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_experience.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_bad_skills(self):
        """POSITIVE: validate with bad skills section reports issues."""
        expected = (
            "Overall: 🔴 Poor (28/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Skills             🔴   8/20  ✖ Skills section should contain technical keywords (tools, languages, frameworks)\n"
            "  Experience         🔴   0/20  ✖ Work Experience section should not be empty\n"
            "  Education          🔴   0/20  ✖ Education section should not be empty\n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_skills.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_bad_all_sections(self):
        """POSITIVE: validate with multiple bad sections reports top issue per section."""
        expected = (
            "Overall: 🔴 Poor (8/80)\n"
            "\n"
            "  Header             🔴   0/20  ✖ A Resume should contain the applicants full name at the start (top) of the document\n"
            "  Experience         🔴   0/20  ✖ Each role should include company name and role title\n"
            "  Skills             🔴   8/20  ✖ Skills section should contain technical keywords (tools, languages, frameworks)\n"
            "  Education          🔴   0/20  ✖ Education section should not be empty\n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_all.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_bad_education(self):
        """POSITIVE: validate with bad education section reports issues."""
        expected = (
            "Overall: 🔴 Poor (25/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Education          🔴   5/20  ✖ Education should include a degree type (e.g. BSc, MSc, PhD)\n"
            "  Experience         🔴   0/20  ✖ Work Experience section should not be empty\n"
            "  Skills             🔴   0/20  ✖ Skills section should not be empty\n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_education.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_needs_work(self):
        """POSITIVE: validate with minor issues produces Needs Work rating."""
        expected = (
            "Overall: 🟡 Needs Work (62/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Experience         🟢  17/20  ⚠ Bullet points should start with strong action verbs (e.g. built, delivered, improved)\n"
            "  Education          🔴   5/20  ✖ Education should include a degree type (e.g. BSc, MSc, PhD)\n"
            "  Skills             🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "needs_work.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_all_required_sections_scored_when_missing(self):
        """POSITIVE: a resume with only a header still scores all required sections as 0/20."""
        expected = (
            "Overall: 🔴 Poor (20/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Experience         🔴   0/20  ✖ Work Experience section should not be empty\n"
            "  Education          🔴   0/20  ✖ Education section should not be empty\n"
            "  Skills             🔴   0/20  ✖ Skills section should not be empty\n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "header_only.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_no_header(self):
        """POSITIVE: resume starting with a section heading scores header as 0/20."""
        expected = (
            "Overall: 🟡 Needs Work (60/80)\n"
            "\n"
            "  Header             🔴   0/20  ✖ A Resume should contain the applicants full name at the start (top) of the document\n"
            "  Experience         🟢  20/20  \n"
            "  Skills             🟢  20/20  \n"
            "  Education          🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "no_header.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_optional_sections_ignored(self):
        """POSITIVE: optional sections (Summary, References) are not scored or shown in output."""
        expected = (
            "Overall: 🟢 Good (80/80)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Experience         🟢  20/20  \n"
            "  Education          🟢  20/20  \n"
            "  Skills             🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "with_optional_sections.txt"))
        assert result.returncode == 0
        assert result.stdout == expected
        assert "Summary" not in result.stdout
        assert "References" not in result.stdout


class TestParseArgs:
    def test_positive_validate_command(self):
        """POSITIVE: validate command with --input is parsed correctly."""
        args = _parse_args(["validate", "--input", "resume.txt"])
        assert args.command == "validate"
        assert args.input == "resume.txt"

    def test_negative_no_command(self):
        """NEGATIVE: no arguments results in command=None."""
        args = _parse_args([])
        assert args.command is None

    def test_negative_validate_missing_input(self):
        """NEGATIVE: validate without --input raises SystemExit."""
        with pytest.raises(SystemExit):
            _parse_args(["validate"])


class TestValidate:
    def test_positive_good_resume(self):
        """POSITIVE: good resume text returns full score output."""
        text = (EXAMPLES_DIR / "good_header.txt").read_text()
        result = _validate(text)
        assert "80/80" in result
        assert "Header" in result
        assert "Experience" in result

    def test_positive_bad_resume(self):
        """POSITIVE: bad resume text returns issues in output."""
        text = (EXAMPLES_DIR / "bad_all.txt").read_text()
        result = _validate(text)
        assert "Poor" in result
        assert "✖" in result

    def test_positive_empty_sections_scored(self):
        """POSITIVE: resume with only header still scores missing required sections."""
        text = (EXAMPLES_DIR / "header_only.txt").read_text()
        result = _validate(text)
        assert "Experience" in result
        assert "Education" in result
        assert "Skills" in result
        assert "0/20" in result

    def test_negative_empty_text_raises(self):
        """NEGATIVE: empty text raises ValueError."""
        with pytest.raises(ValueError):
            _validate("")
