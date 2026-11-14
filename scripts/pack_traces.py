"""Back up per-question traces that are no longer kept in git.

    python scripts/pack_traces.py                 # every run under runs/test
    python scripts/pack_traces.py runs/test/2026...   # only these runs
    python scripts/pack_traces.py --restore-pulled    # after a `git pull` that untracked them

trace.jsonl / explorer.json / tree.svg are ignored by git (Git LFS quota). This writes
one runs/_traces/<run>.tar.xz per run, skipped when the archive is newer than every
file in it. Copy runs/_traces/ wherever backups live (NAS, external disk).

--restore-pulled: a pull that removes these files from git also deletes them from the
working tree. This puts them back from the previous commit (ORIG_HEAD, set by the
pull) without tracking them again; the LFS objects are already on this machine.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = {"trace.jsonl", "explorer.json", "tree.svg"}


def run_files(run: Path) -> list[Path]:
    return sorted(p for p in run.rglob("*") if p.is_file() and p.name in NAMES)


def pack(run: Path, out_dir: Path) -> str:
    files = run_files(run)
    if not files:
        return "no traces"
    archive = out_dir / f"{run.name}.tar.xz"
    if archive.exists() and archive.stat().st_mtime >= max(p.stat().st_mtime for p in files):
        return "up to date"
    temporary = archive.with_suffix(".xz.tmp")
    with tarfile.open(temporary, "w:xz") as tar:
        for path in files:
            tar.add(path, arcname=str(path.relative_to(run.parent)))
    temporary.replace(archive)
    raw = sum(p.stat().st_size for p in files)
    return f"{len(files)} files, {raw / 1e6:,.0f} MB -> {archive.stat().st_size / 1e6:,.0f} MB"


def restore_pulled(source: str) -> int:
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                              text=True, encoding="utf-8").stdout
    removed = [p for p in git("diff", "--name-only", "--diff-filter=D", source, "HEAD", "--", "runs").splitlines()
               if Path(p).name in NAMES and not (ROOT / p).exists()]
    if not removed:
        print("Nothing to restore.")
        return 0
    for start in range(0, len(removed), 200):
        subprocess.run(["git", "restore", f"--source={source}", "--worktree", "--", *removed[start:start + 200]],
                       cwd=ROOT, check=True)
    print(f"Restored {len(removed)} files from {source}; they stay untracked (ignored).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", nargs="*", type=Path, help="run directories (default: all of runs/test)")
    parser.add_argument("--out", type=Path, default=ROOT / "runs" / "_traces")
    parser.add_argument("--restore-pulled", nargs="?", const="ORIG_HEAD", metavar="REV",
                        help="restore files a pull removed from git (default ORIG_HEAD)")
    args = parser.parse_args(argv)
    if args.restore_pulled:
        return restore_pulled(args.restore_pulled)
    runs = args.runs or sorted(p for p in (ROOT / "runs" / "test").iterdir() if p.is_dir())
    args.out.mkdir(parents=True, exist_ok=True)
    for run in runs:
        print(f"{run.name}: {pack(run, args.out)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
