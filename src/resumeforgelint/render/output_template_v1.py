
SUMMARY = 'Overall: {emoji} {rating} ({total}/100)'
SECTION = '  {name:<18} {emoji}  {score:>2}/20  {issue}'

class OutputTemplateV1:
    """Takes overall and section scores for a resume and renders a pretty text report."""

    def __init__(self):
        self.summary_text: str | None  = None
        self.sections: list[str] = []

    def summary(self, props: dict[str, str]) -> "OutputTemplateV1":
        self.summary_text = SUMMARY.format(**props)
        return self
    
    def section(self, props: dict[str, str]) -> "OutputTemplateV1":
        self.sections.append(SECTION.format(**props))
        return self
    
    def render(self) -> str:
        if self.summary_text is None:
            raise ValueError("No replacement was applied for SUMMARY - 1 required")
        if len(self.sections) == 0:
            raise ValueError("No replacements was applied for SECTION - requires at least one.")
        sections_block = "\n".join(self.sections)
        return self.summary_text + "\n\n" + sections_block
