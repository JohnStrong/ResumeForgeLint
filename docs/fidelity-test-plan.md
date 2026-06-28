# Fidelity Test Plan

How to validate that resumes passing ResumeForgeLint are actually parsed correctly by real ATS systems.

## Local Fidelity Testing (spaCy)

We use spaCy's NER model (`en_core_web_sm`) to independently extract structured data from our example resumes and compare against ResumeForgeLint's scoring output.

### Setup

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Run

```bash
python scripts/fidelity_test.py
```

### What it checks

| Section | spaCy extraction | Validates |
|---------|-----------------|-----------|
| Header | PERSON entities, email regex, phone regex | Name/email/phone rubrics |
| Experience | ORG entities, date range regex | Company/role and date rubrics |
| Education | Degree regex, institution keywords | Degree and institution rubrics |
| Skills | Token count (nouns/proper nouns) | Keyword density rubric |

### Interpretation

If spaCy cannot extract a field (e.g. no PERSON entity found), our tool should flag it as a critical issue. If spaCy finds it, our tool should score it as passing.

## Free Online ATS Parsers

- **Jobscan** (jobscan.co) — free tier lets you upload a resume and see how it parses against a job description
- **Resume Worded** (resumeworded.com) — free score with breakdown of what was detected/missing

## Gold Standard Comparison

- **Create a free employer account on Greenhouse or Lever** (both have free trials). Upload test resumes as if you're a hiring manager. You'll see exactly how their ATS parsed each field.

## Deprecated

- **pyresparser** — last updated 2019, incompatible with Python 3.10+ and spaCy 3.x. Do not use.
