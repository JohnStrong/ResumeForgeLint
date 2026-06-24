from resumeforgelint.models import Section, SectionType

_SYNONYMS: dict[SectionType, list[str]] = {
    SectionType.SUMMARY: ["summary", "profile", "objective", "about me"],
    SectionType.EXPERIENCE: ["experience", "work experience", "work history", "employment", "professional experience"],
    SectionType.EDUCATION: ["education", "academics", "qualifications"],
    SectionType.SKILLS: ["skills", "technical skills", "core competencies", "competencies"],
    SectionType.REFERENCES: ["references"],
}

def _match_heading(line: str) -> SectionType | None:
    normalized = line.strip().lower()
    for section_type, synonyms in _SYNONYMS.items():
        if normalized in synonyms:
            return section_type
    return None

def parse(resume_text: str) -> list[Section]:
    """Parse the resume text into well-known sections ready for scoring later."""
    if not resume_text:
        raise ValueError("Cannot score an empty Resume")

    sections: list[Section] = []
    current_type = SectionType.HEADER
    current_heading: str | None = None
    current_content: list[str] = []

    lines = resume_text.splitlines()
    for line in lines:
        matched = _match_heading(line)
        if matched:
            sections.append(Section(current_type, current_heading, current_content))
            current_type = matched
            current_heading = line.strip()
            current_content = []
        else:
            current_content.append(line)

    sections.append(Section(current_type, current_heading, current_content))
    return sections
