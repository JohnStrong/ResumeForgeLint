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

## Commands

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
