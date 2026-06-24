from collections.abc import Callable

from resumeforgelint.models import SectionType, Section, ScoredSection
from resumeforgelint.scorer import score_header

SCORERS: dict[SectionType, Callable[[Section], ScoredSection]] = {
    SectionType.HEADER: score_header,
}