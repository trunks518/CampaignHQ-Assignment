from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_summary_basic(tmp_path: Path) -> None:
    csv_bytes = (
        b"id,status,ts,notes\n"
        b"1,success,2024-01-01T00:00:00Z,a\n"
        b"1,success,2024-01-01T00:00:00Z,dup\n"
        b"2,fail,2024-02-01T00:00:00+00:00,b\n"
        b"3,unknown,2024-03-01T12:34:56,c\n"
        b"4,invalid,2024-04-01T09:00:00Z,d\n"
        b",success,2024-01-01T00:00:00Z,e\n"
        b"5,success,not-a-date,f\n"
    )

    files = {"file": ("data.csv", csv_bytes, "text/csv")}
    res = client.post("/api/results/upload", files=files)
    assert res.status_code == 200, res.text

    data = res.json()
    assert data["total_rows"] == 7
    assert data["valid_rows"] == 3
    assert data["by_status"]["success"] == 1
    assert data["by_status"]["fail"] == 1
    assert data["by_status"]["unknown"] == 1
    assert len(data["errors"]) == 3

