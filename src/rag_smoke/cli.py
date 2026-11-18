from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from rag_smoke.smoke import run_smoke, write_report

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rag-smoke")
    parser.add_argument("--workspace", default="..")
    parser.add_argument("--results", default="results")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).resolve()
    report = run_smoke(workspace)
    write_report(report, Path(args.results))

    table = Table(title="RAG Smoke Local")
    table.add_column("repo")
    table.add_column("ok")
    table.add_column("missing")
    for item in report["details"]:
        table.add_row(
            item["repo"],
            "yes" if item["ok"] else "no",
            ", ".join(item["missing"]) or "—",
        )
    console.print(table)
    console.print(f"score: [bold]{report['score']:.0%}[/bold] ({report['passed']}/{report['total']})")
    return 0 if report["score"] >= 0.9 else 1


if __name__ == "__main__":
    raise SystemExit(main())
