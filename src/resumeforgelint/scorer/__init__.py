from resumeforgelint.scorer.scorer import score
from resumeforgelint.scorer.header_rubrics import RUBRICS as HEADER_RUBRICS
from resumeforgelint.scorer.work_experience_rubrics import RUBRICS as EXPERIENCE_RUBRICS
from resumeforgelint.models import SectionType, ScoringRubric

MAPPER: dict[SectionType, list[ScoringRubric]] = {
    SectionType.HEADER: HEADER_RUBRICS,
    SectionType.EXPERIENCE: EXPERIENCE_RUBRICS
}
