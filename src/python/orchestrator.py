"""Plan an InDesign batch from config. Does not open InDesign."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if "jobs" not in data or not isinstance(data["jobs"], list):
        raise ValueError("config must contain a jobs list")
    return data


def plan(config: dict[str, Any], force: bool = False) -> list[dict[str, Any]]:
    """Return jobs that still need to run.

    A job is skipped when runs/<id>.json exists and status is done,
    unless force is True.
    """
    runs = Path(config.get("runs_dir", "runs"))
    pending: list[dict[str, Any]] = []
    for job in config["jobs"]:
        job_id = str(job["id"])
        status_path = runs / f"{job_id}.json"
        if status_path.exists() and not force:
            status = json.loads(status_path.read_text(encoding="utf-8"))
            if status.get("status") == "done":
                continue
        pending.append(
            {
                "id": job_id,
                "xml": job["xml"],
                "template": config["template"],
                "output": str(Path(config.get("output_dir", "out")) / f"{job_id}.indd"),
                "style_map": config.get("style_map", {}),
            }
        )
    return pending


def write_manifest(pending: list[dict[str, Any]], dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(pending, indent=2), encoding="utf-8")
