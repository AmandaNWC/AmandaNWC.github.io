# Academic CV source

The website's existing `NaiWen_Chi_CV.pdf` is generated from `cv/cv.json` with `cv/build_cv.py`.

Install Python 3 and ReportLab, then run from the repository root:

```
python -m pip install reportlab
python cv/build_cv.py
```

An optional first argument selects another output path. The source uses standard PDF fonts and A4 pages. Keep the output to two pages, check all hyperlinks, and visually inspect both pages after edits. Education and employment facts are retained from the existing applicant CV. Journal citations and public patent identifiers were checked on October 21, 2026. Do not infer experimental leadership from co-authorship, current enforceability from a patent publication, an award from a submitted grant, or completed peer reviews from reviewer registration.
