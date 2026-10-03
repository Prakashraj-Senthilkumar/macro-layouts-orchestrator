# macro-layouts-orchestrator

Config-driven publishing automation skeleton: a Python orchestrator plans a batch, and an ExtendScript worker applies layout inside InDesign.

This is the Macro Layouts pattern in miniature. Business rules stay in `config/`. Scripts stay restartable. The Adobe layer does not decide pagination policy.

## Layout

```
macro-layouts-orchestrator/
├── README.md
├── .gitignore
├── requirements.txt
├── config/
│   └── settings.example.json
├── src/
│   ├── python/orchestrator.py
│   └── extendscript/apply_layout.jsx
├── scripts/run_batch.py
└── tests/test_plan.py
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy config\settings.example.json config\settings.json
python scripts/run_batch.py --config config/settings.json --dry-run
```

`--dry-run` writes a job manifest and does not launch InDesign. Drop `--dry-run` only on a machine with InDesign installed; the worker is invoked with `os.startfile` / a configured executable path.

## Contract

Input: a folder of `.xml` or `.idml` jobs listed in config.
Output: one JSON status file per job under `runs/`, plus the InDesign document the worker saves.

Re-running a batch skips jobs whose status is `done` unless `--force` is passed.

## Limits

The ExtendScript worker is a safe starter. It opens a template, places the XML file named in the job, applies a paragraph style map from config, saves, and closes. It does not paginate complex math or touch master pages beyond what the template already defines.
