from dataclasses import dataclass
from enum import StrEnum

class Severity(StrEnum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Issue:
    """Represents an Issue with a Scored Section with its severity to address"""
    severity: Severity
    message: str  # user message to output

class SectionType(StrEnum):
    HEADER = "header"
    SUMMARY = "summary"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    REFERENCES = "references"
    UNKNOWN = "unknown"
  

@dataclass
class Section:
    """Represents a Resume section boundary with heading, and its content for scoring."""
    section_type: SectionType
    heading: str | None # None only for the implicit header section
    content: list[str]  # empty list if no content

@dataclass
class ScoredSection:
    """Represents a scored (0 -> 20) Resumed section against the scoring 'rubrics' applied.

    We score 5 well-known sections (today), so total score is out-of 100 implicitely:
        Skills          
        Work Experience  
        Education       
        Summary          
        References
    """
    section: Section
    score: int
    issues: list[Issue]
