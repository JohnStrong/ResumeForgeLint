# ResumeForgeLint
Simple ATS (application tracking system) Resume/C.V validation tool

> **Companion tool:** [ResumeForge](https://resume-forge-cli.web.app/) — generate ATS-friendly resumes

## Table of Contents

- [Features (v1)](#features-v1)
- [Scoring Rubrics](#scoring-rubrics-work-in-progress)
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

## Scoring Rubrics (Work in progress)

> `[x]` denotes rubric is implemented

### Header (20 points)
- [x] Full name present on first line
- [x] Email address present
- [x] Phone number present
- [x] Phone number country code present (e.g. +1, +44)
- [ ] LinkedIn URL present (optional, bonus)

### Work Experience (20 points)
- [x] Section present
- [x] Quantified achievements (numbers, percentages, metrics)
- [x] Action verbs at start of bullet points
- [x] Date ranges present for each role
- [x] Company and role title present

### Skills (20 points)
- [ ] Section present
- [ ] Contains keywords (technical terms, tools, languages)
- [ ] Minimum keyword count threshold
- [ ] No excessive soft-skill filler

### Education (20 points)
- [ ] Section present
- [ ] Degree type present (BSc, MSc, PhD, etc.)
- [ ] Institution name present
- [ ] Graduation date present

### Summary/Profile (20 points)
- [ ] Section present
- [ ] Minimum length (not too short)
- [ ] Maximum length (not too long)
- [ ] Contains relevant keywords

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

## Examples

> **Note:** Output is subject to change as not all section scorers are implemented yet. Currently only the Header section is scored.

### Good header (`examples/good_header.txt`)

```bash
$ resumeforgelint validate --input examples/good_header.txt
```

```
Overall: 🔴 Poor (20/100)

  Header             🟢  20/20
```

### Bad header (`examples/bad_header.txt`)

```bash
$ resumeforgelint validate --input examples/bad_header.txt
```

```
Overall: 🔴 Poor (10/100)

  Header             🟡  10/20  ✖ A Resume should contain the applicants full name at the start (top) of the document
```
