# ResumeForgeLint
Simple ATS (application tracking system) Resume/C.V validation tool

## Features (v1)

- **Validate a resume provided as a `.txt` file**
- **Fuzzy section heading detection** using synonym sets (e.g., Experience/Work History/Employment; Education/Academics; Skills/Technical Skills)
- **Per-section rubric scoring + issue reporting**
  - Shows which sections/signals were detected
  - Lists issues with severity (critical/warning/info) and short "why" explanations
- **Machine-readable output**
  - `--json` prints a structured report (scores, matched signals, issue list)
- **Human-readable output**
  - Default mode prints a summary of ATS risk + recommended fixes
- **Required-section expectations (baseline)**
  - Core sections expected (scored even if missing):
    - Work Experience
    - Skills
    - Education
  - Optional sections graded only if present:
    - Profile/Summary
    - References
