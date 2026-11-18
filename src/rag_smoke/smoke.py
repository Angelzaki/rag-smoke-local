from __future__ import annotations

import json
from pathlib import Path

CORE = [
    "rag-eval-platform",
    "local-rag-pipeline",
    "local-ai-agents",
    "chunk-lab",
    "retrieval-tuner-local",
    "abstention-lab-local",
    "context-overlap-lab",
    "faithfulness-guard",
    "citation-auditor-local",
    "prompt-bench-local",
    "rag-trace-local",
    "synthetic-qa-local",
    "doc-drift-lab",
    "eval-hub-local",
    "llm-cost-radar",
    "prompt-firewall",
    "model-router-local",
    "agent-failure-lab",
    "llm-ci-gates",
    "support-copilot-lab",
]

REQUIRED_FILES = {
    "rag-eval-platform": ["pyproject.toml", "samples/ground_truth/questions.jsonl", "README.md"],
    "local-rag-pipeline": ["pyproject.toml", "src/local_rag/pipeline.py", "README.md"],
    "local-ai-agents": ["pyproject.toml", "src/local_agents/router.py", "README.md"],
    "eval-hub-local": ["pyproject.toml", "src/eval_hub/collect.py", "README.md"],
}


def check_repo(workspace: Path, name: str) -> dict:
    root = workspace / name
    item = {"repo": name, "exists": root.exists(), "ok": False, "missing": []}
    if not root.exists():
        item["missing"].append("repo")
        return item

    required = REQUIRED_FILES.get(name, ["pyproject.toml", "README.md"])
    for rel in required:
        if not (root / rel).exists():
            item["missing"].append(rel)

    src_dirs = list(root.glob("src/*"))
    if not src_dirs:
        item["missing"].append("src_package")

    tests = list((root / "tests").glob("test_*.py")) if (root / "tests").exists() else []
    if not tests:
        item["missing"].append("tests")

    item["ok"] = len(item["missing"]) == 0
    return item


def run_smoke(workspace: Path) -> dict:
    details = [check_repo(workspace, name) for name in CORE]
    # also include self if present
    if (workspace / "rag-smoke-local").exists():
        details.append(check_repo(workspace, "rag-smoke-local"))
    passed = sum(1 for d in details if d["ok"])
    return {
        "passed": passed,
        "total": len(details),
        "score": round(passed / len(details), 4) if details else 0.0,
        "details": details,
    }


def write_report(report: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "smoke_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
