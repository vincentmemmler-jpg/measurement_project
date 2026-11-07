# Measurement project

Summarize synthetic measurements above a chosen threshold.

## Purpose

The project answers one question: **how many measurements are strictly greater than a threshold?** It also reports the number of measurements and their mean.

The threshold rule is strict: a value counts only if `value > threshold`. A value equal to the threshold is **not** counted.

Experiments are defined by YAML files in `config/`. Changing the YAML changes the experiment; the Python code stays the same.

## Setup

Requires Python 3.11 or later. Create and activate a project environment, then install the package from the project root:

```bash
conda create -n measurement python=3.12 -y
conda activate measurement
python -m pip install -e .
```

Check that the terminal uses the environment's interpreter:

```bash
python -c "import sys; print(sys.executable)"
```

The path should end in `envs/measurement/bin/python`. In VS Code or Jupyter, select the same environment.

## Run

Run from the project root:

```bash
python -m course_project.pipeline --config config/base.yaml
python -m course_project.pipeline --config config/high_threshold.yaml
```

The `--config` path is relative to the current terminal directory. Paths **inside** a YAML file are relative to that YAML file, so an absolute `--config` path works from any directory.

In a notebook, call the function instead of the command line:

```python
from course_project.pipeline import run
run("config/base.yaml")
```

## Input and output

| Item | Location | Notes |
|---|---|---|
| Input | `data/raw/measurements.csv` | Read-only raw data |
| Configuration | `config/*.yaml` | `input_path`, `output_dir`, `analysis.column`, `analysis.threshold` |
| Output | `outputs/<experiment>/summary.json` | Generated; ignored by Git |

Input columns:

| Column | Meaning |
|---|---|
| `sample_id` | Sample identifier (not used in the calculation) |
| `value` | Numeric measurement; must be finite |

Output fields: `n` (number of values), `mean`, `n_above` (values strictly above the threshold), and `threshold`.

## Verification

Expected results for the synthetic example (values 8, 10, 12, 14):

| Configuration | Threshold | `n` | `mean` | `n_above` |
|---|---|---|---|---|
| `config/base.yaml` | 10.0 | 4 | 11.0 | 2 |
| `config/high_threshold.yaml` | 12.0 | 4 | 11.0 | 1 |

Invalid configurations fail before any data is read: a Boolean, a quoted string, or an infinite threshold raises `ValueError`.

## Project structure

```
measurement_project/
├── README.md
├── pyproject.toml          # package name, Python version, dependencies
├── .gitignore
├── config/                 # experiment settings (YAML)
├── data/raw/               # raw input, never edited
├── outputs/                # generated results (not in Git)
└── src/course_project/
    ├── config.py           # load, validate, and resolve the YAML
    ├── io.py               # read CSV, write JSON
    ├── analysis.py         # pure calculations
    └── pipeline.py         # connects the steps; command-line entry point
```

## Attribution and limitations

The measurements are small synthetic teaching data created for this course. No external data or code is included. The analysis reads one numeric column and does not handle missing values: any empty, `nan`, or non-numeric cell stops the run with an error.
