import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from orchestrator import plan


def test_skips_done_jobs(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "J001.json").write_text(json.dumps({"status": "done"}), encoding="utf-8")
    config = {
        "template": "t.indt",
        "runs_dir": str(runs),
        "output_dir": str(tmp_path / "out"),
        "jobs": [{"id": "J001", "xml": "a.xml"}, {"id": "J002", "xml": "b.xml"}],
    }
    pending = plan(config)
    assert [job["id"] for job in pending] == ["J002"]
