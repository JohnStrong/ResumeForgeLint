# ResumeForgeLint
Simple ATS (application tracking system) Resume/C.V validation tool

> **Documentation:** [resume-forge-lint.web.app](https://resume-forge-lint.web.app/)

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
  - Unrecognized sections (e.g. Projects, Volunteer Work, Certifications) are ignored and do not contribute to the score

> **Note:** Profile/Summary and References are not scored in v1. Most ATS systems do not parse these sections for structured data, and modern best practice is to omit References entirely. They do not contribute to the score positively or negatively.

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
- [x] Section present
- [x] Contains keywords (technical terms, tools, languages)
- [x] Minimum keyword count threshold
- [x] No excessive soft-skill filler

### Education (20 points)
- [x] Section present
- [x] Degree type present (BSc, MSc, PhD, etc.)
- [x] Institution name present
- [x] Graduation date present

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
Overall: 🟢 Good (80/80)

  Header             🟢  20/20
  Experience         🟢  20/20
  Education          🟢  20/20
  Skills             🟢  20/20
```

## Examples

### Good resume (`examples/good_header.txt`)

All required sections present with complete information. Scores 80/80 (100%).

```bash
$ resumeforgelint validate --input examples/good_header.txt
```

```
Overall: 🟢 Good (80/80)

  Header             🟢  20/20
  Experience         🟢  20/20
  Education          🟢  20/20
  Skills             🟢  20/20
```

### Needs Work (`examples/needs_work.txt`)

Has all sections but Education is missing degree type and institution. Experience lacks action verbs. Scores 62/80 (77%).

```bash
$ resumeforgelint validate --input examples/needs_work.txt
```

```
Overall: 🟡 Needs Work (62/80)

  Header             🟢  20/20
  Experience         🟢  17/20  ⚠ Bullet points should start with strong action verbs (e.g. built, delivered, improved)
  Education          🔴   5/20  ✖ Education should include a degree type (e.g. BSc, MSc, PhD)
  Skills             🟢  20/20
```

### Poor resume (`examples/bad_all.txt`)

Missing name in header, no company/role or dates in experience, no technical keywords in skills, and no education section content. Scores 8/80 (10%).

```bash
$ resumeforgelint validate --input examples/bad_all.txt
```

```
Overall: 🔴 Poor (8/80)

  Header             🔴   0/20  ✖ A Resume should contain the applicants full name at the start (top) of the document
  Experience         🔴   0/20  ✖ Each role should include company name and role title
  Skills             🔴   8/20  ✖ Skills section should contain technical keywords (tools, languages, frameworks)
  Education          🔴   0/20  ✖ Education section should not be empty
```
