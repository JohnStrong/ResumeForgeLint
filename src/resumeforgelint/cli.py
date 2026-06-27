import argparse
import sys
from pathlib import Path

from resumeforgelint.parser.section_parser import parse
from resumeforgelint.scorer.scorer import score
from resumeforgelint.scorer import MAPPER
from resumeforgelint.render.renderer import render


def main():
    parser = argparse.ArgumentParser(prog="resumeforgelint", description="ATS Resume validation tool")
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="Validate a plain-text resume")
    validate_parser.add_argument("--input", required=True, help="Path to .txt resume file")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "validate":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: file not found: {args.input}")
            sys.exit(1)

        text = input_path.read_text()
        sections = parse(text)

        # Score each section (only header scorer implemented for now)
        scored_sections = []
        for section in sections:
            if section.section_type in MAPPER:
                scored_sections.append(score(section, MAPPER[section.section_type]))

        if scored_sections:
            print(render(scored_sections))
