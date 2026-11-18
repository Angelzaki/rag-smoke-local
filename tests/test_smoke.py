from pathlib import Path

from rag_smoke.smoke import check_repo, run_smoke


def test_check_missing_repo(tmp_path):
    item = check_repo(tmp_path, "no-existe")
    assert item["ok"] is False


def test_run_against_workspace():
    workspace = Path(__file__).resolve().parents[2]
    report = run_smoke(workspace)
    assert report["total"] >= 10
    assert report["score"] >= 0.8
