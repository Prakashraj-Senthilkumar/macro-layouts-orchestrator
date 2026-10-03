"""Entry point. Dry-run writes a manifest and does not launch InDesign."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from orchestrator import load_config, plan, write_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan a Macro Layouts batch")
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    pending = plan(config, force=args.force)
    manifest = Path(config.get("runs_dir", "runs")) / "manifest.json"
    write_manifest(pending, manifest)
    print(f"{len(pending)} job(s) pending -> {manifest}")
    if not args.dry_run:
        print("Live InDesign launch is not wired in this starter. Use --dry-run.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
