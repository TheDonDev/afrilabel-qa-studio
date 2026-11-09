
# AfriLabel QA Studio
### A lightweight quality-control tool for AI image-annotation datasets

AfriLabel QA Studio checks COCO-style object-detection annotations and produces a readable quality report. It is a portfolio demonstration of annotation quality assurance, Python, structured-data validation, and reproducible testing.

> **Data note:** The included dataset is synthetic demonstration data. The image filenames are placeholders; no real photographs or personal data are included.

## Why this project matters

An object-detection model learns from the labels it receives. Incorrect categories, invalid bounding boxes, and boxes outside image boundaries can reduce dataset quality. This tool catches common structural problems before a dataset moves to the next stage.

## Features

- Validates bounding-box format: `[x, y, width, height]`
- Flags zero or negative box dimensions
- Flags boxes that extend beyond image dimensions
- Detects unknown image and category references
- Flags possible duplicate annotations
- Summarises class distribution
- Exports machine-readable JSON and spreadsheet-friendly CSV reports
- Includes unit tests for clean and problematic datasets

## Requirements

- Python 3.9 or newer
- No third-party Python packages required

## Run it

Clone the repository, then from its root directory:

```bash
python3 afrilabel_qa.py sample_data/sample_annotations.json
```

The command creates a `reports/` directory containing:

- `qa_report.json` — complete validation summary and issues
- `qa_issues.csv` — issue list suitable for spreadsheet review

The sample intentionally includes a few problems so you can see the checker working. A `FAIL` result on the sample is expected.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

## Example output

```text
AfriLabel QA Studio: FAIL
Images checked: 3
Annotations checked: 7
Errors: 2 | Warnings: 2
Reports saved to: .../reports
```

Exact issue counts are determined by the validator and sample data.

## Supported input structure

The input follows the core structure of a COCO object-detection JSON file:

- `images`: image IDs, filenames, width and height
- `categories`: category IDs and names
- `annotations`: image ID, category ID and bounding box

This first version focuses on bounding-box dataset checks. It does not inspect image pixels, decide whether an object is correctly labelled, or replace human review.

## Project structure

```text
afrilabel-qa-studio/
├── afrilabel_qa.py
├── sample_data/
│   └── sample_annotations.json
├── tests/
│   └── test_validator.py
├── .gitignore
├── LICENSE
└── README.md
```

## Skills demonstrated

Python · JSON · CSV · Data validation · Object-detection annotations · Bounding boxes · QA reporting · Unit testing · Git

## Possible next improvements

- Add visual bounding-box previews when source images are available
- Add configurable project-specific annotation rules
- Add a small Streamlit dashboard for reviewing issues
- Add support for segmentation masks and other annotation formats

## Author

**Donald Mwanga Makori**  
Computer Science graduate | Data Annotation | Computer Vision | Software QA

- GitHub: https://github.com/TheDonDev
- Portfolio: https://thedondev.github.io.

---

Built as an independent portfolio project. It is not affiliated with, or endorsed by, any employer or annotation platform.
