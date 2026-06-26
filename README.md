# ResumeForgeLint
Simple ATS (application tracking system) Resume/C.V validation tool

> **Companion tool:** [ResumeForge](https://resume-forge-cli.web.app/) — generate ATS-friendly resumes

## Table of Contents

- [Features (v1)](#features-v1)
- [Commands](#commands)
  - [`validate`](#validate)

## Features (v1)

- **Validate a resume provided as a `.txt` file**
- **Fuzzy section heading detection** using synonym sets (e.g., Experience/Work History/Employment; Education/Academics; Skills/Technical Skills)
- **Per-section rubric scoring + issue reporting**
  - Shows which sections/signals were detected
  - Lists issues with severity (critical/warning/info) and short "why" explanations
- **Human-readable output**
  - Default mode prints a summary of ATS risk + top issues per section
- **Required-section expectations (baseline)**
  - Core sections expected (scored even if missing):
    - Work Experience
    - Skills
    - Education
  - Optional sections graded only if present:
    - Profile/Summary
    - References

## Commands

### `validate`

Analyse a `.txt` resume, score each section, and print a summary report.

```bash
resumeforgelint validate --input resume.txt
```

**What it does:**

1. Reads the plain-text resume
2. Detects sections via fuzzy heading matching (synonym sets)
3. Scores each section and flags issues (critical / warning / info)
4. Prints a summary to stdout:
   - Overall rating (🟢 Good / 🟡 Needs Work / 🔴 Poor)
   - Per-section breakdown with score and top issue

**Example output:**

```
Overall: 🟡 Needs Work (62/100)

  Skills             🟢  18/20
  Work Experience    🟡  14/20  ⚠ missing quantified achievements
  Education          🟢  16/20
  Summary            🔴   6/20  ✖ too short, no keywords
  Header             🟢  20/20
```
