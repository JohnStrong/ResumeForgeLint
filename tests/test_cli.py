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
        """POSITIVE: validate with good header resume produces full score for header."""
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "good_header.txt"))
        assert result.returncode == 0
        assert "20/20" in result.stdout
        assert "Header" in result.stdout

    def test_positive_validate_bad_header(self):
        """POSITIVE: validate with bad header resume reports issue."""
        result = _run_cli("validate", "--input", str(EXAMPLES_DIR / "bad_header.txt"))
        assert result.returncode == 0
        assert "10/20" in result.stdout
        assert "full name" in result.stdout.lower()

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
