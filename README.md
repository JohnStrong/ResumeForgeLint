# ResumeForgeLint
Simple ATS (application tracking system) Resume/C.V validation tool

> **Companion tool:** [ResumeForge](https://resume-forge-cli.web.app/) — generate ATS-friendly resumes

## Table of Contents

- [Features (v1)](#features-v1)
- [Commands](#commands)
  - [`validate`](#validate)
- [Milestones](#milestones)
  - [M1 — CLI skeleton & section detection](#m1--cli-skeleton--section-detection)
  - [M2 — Section scoring rubrics](#m2--section-scoring-rubrics)
  - [M3 — Issue detection & severity classification](#m3--issue-detection--severity-classification)
  - [M4 — JSON report output](#m4--json-report-output)
  - [M5 — Colorized stdout summary](#m5--colorized-stdout-summary)
  - [M6 — Polish & packaging](#m6--polish--packaging)

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

## Commands (Planned)

### `validate`

Analyse a `.txt` resume, score each section, and produce a JSON report.

```bash
resumeforgelint validate --input resume.txt
```

**What it does:**

1. Reads the plain-text resume
2. Detects sections via fuzzy heading matching (synonym sets)
3. Scores each section and flags issues (critical / warning / info)
4. Prints a colorized summary to stdout:
   - Overall rating (🟢 Good / 🟡 Needs Work / 🔴 Poor)
   - Per-section breakdown with color (green/yellow/red) and key issues
5. Writes a JSON report to the current directory and prints its path

**Example output:**

```
Overall: 🟡 Needs Work (62/100)

  Skills           🟢  18/20
  Work Experience  🟡  14/20  ⚠ missing quantified achievements
  Education        🟢  16/20
  Summary          🔴   6/20  ✖ too short, no keywords
  References       —   not found (optional)

Report saved: ./resumeforgelint-report-20260620-001700.json
```

**Planned additions:**

- `--format html` — generate an HTML report (future)

## Milestones

### M1 — CLI skeleton & section detection
- [ ] Set up CLI entry point (`validate --input`)
- [ ] Parse `.txt` input and split into raw lines
- [ ] Implement fuzzy heading matcher with synonym sets
- [ ] Return list of detected sections with line ranges

### M2 — Section scoring rubrics
- [ ] **Work Experience** rubric — quantified achievements, action verbs, date ranges, bullet structure
- [ ] **Skills** rubric — keyword density, categorization, relevance signals
- [ ] **Education** rubric — degree present, institution, dates, GPA/honors (optional)
- [ ] **Summary/Profile** rubric — length, keyword alignment, clarity
- [ ] **References** rubric — presence check only (optional section)
- [ ] Score normalization (each section out of 20, total out of 100)

### M3 — Issue detection & severity classification
- [ ] Define issue catalog (critical / warning / info) per rubric
- [ ] Attach issues to scored sections with short "why" explanations
- [ ] Compute overall rating threshold (Good ≥ 80 / Needs Work ≥ 50 / Poor < 50)

### M4 — JSON report output
- [ ] Define standardized report schema (version, metadata, sections[], issues[], scores)
- [ ] Serialize report and write to cwd with timestamped filename
- [ ] Print report file path to stdout

### M5 — Colorized stdout summary
- [ ] Overall rating line with emoji + color
- [ ] Per-section table with green/yellow/red and top issue per section
- [ ] Graceful fallback when terminal doesn't support color

### M6 — Polish & packaging
- [ ] End-to-end integration test with sample resume
- [ ] `pip install .` works and `resumeforgelint validate` is available on PATH
- [ ] README examples verified against actual output
