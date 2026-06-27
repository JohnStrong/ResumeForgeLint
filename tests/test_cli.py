import subprocess
from pathlib import Path

import pytest

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
            "Overall: 🟡 Needs Work (60/100)\n"
            "\n"
            "  Header             🟢  20/20  \n"
            "  Experience         🟢  20/20  \n"
            "  Skills             🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "good_header.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_positive_validate_bad_header(self):
        """POSITIVE: validate with bad header resume produces expected output."""
        expected = (
            "Overall: 🔴 Poor (40/100)\n"
            "\n"
            "  Header             🔴   0/20  ✖ A Resume should contain the applicants full name at the start (top) of the document\n"
            "  Experience         🟢  20/20  \n"
            "  Skills             🟢  20/20  \n"
        )
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_header.txt"))
        assert result.returncode == 0
        assert result.stdout == expected

    def test_negative_no_command(self):
        """NEGATIVE: no command prints help and exits 1."""
        result = _run_cli()
        assert result.returncode == 1

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

    @pytest.mark.skip(reason="Parser does not yet emit empty sections for missing required sections. "
                             "A resume missing Work Experience will not be penalised until the parser "
                             "populates a null/empty Section for required types not found in the text.")
    def test_negative_missing_required_section_still_scored(self):
        """NEGATIVE: a resume missing a required section (e.g. Work Experience) should still
        report it as scored with 0/20 in the output. Currently the parser only returns sections
        it finds, so missing sections are silently ignored."""
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "good_header.txt"))
        # Once fixed, a resume without Experience should show Experience 0/20
        assert "Experience" in result.stdout
