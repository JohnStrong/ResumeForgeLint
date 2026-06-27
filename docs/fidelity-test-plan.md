# Fidelity Test Plan

How to validate that resumes passing ResumeForgeLint are actually parsed correctly by real ATS systems.

## Free Online ATS Parsers

- **Jobscan** (jobscan.co) — free tier lets you upload a resume and see how it parses against a job description. Shows which fields were extracted.
- **Resume Worded** (resumeworded.com) — free score with breakdown of what was detected/missing.
- **Pymetrics/HireVue** parser previews — some have free trials showing parsed output.

## Open-Source ATS Parsers (CLI-to-CLI comparison)

- **pyresparser** (`pip install pyresparser`) — Python library that extracts name, email, phone, skills, education using spaCy/NLTK. Run against test resumes and compare what it extracts vs what ResumeForgeLint flags.
- **resume-parser** on GitHub (several variants) — similar extraction, good for spot-checking.

## Gold Standard Comparison

- **Create a free employer account on Greenhouse or Lever** (both have free trials). Upload test resumes as if you're a hiring manager. You'll see exactly how their ATS parsed each field. This is the most realistic fidelity test.

## Recommended Workflow

1. Use `pyresparser` locally for quick automated comparison — if it can't extract a name/email/phone from "bad" examples, our rubrics are validated.
2. Spot-check a few through Jobscan's free tier for real-world ATS confidence.
3. Periodically validate against Greenhouse/Lever free trials for gold-standard fidelity.
