import subprocess
import sys
from pathlib import Path


def test_generate_report(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "generate_report.py"

    data = tmp_path / "data"
    data.mkdir()
    (data / "sample_orders.csv").write_text(
        "price,quantity\n10000,2\n5000,3\n",
        encoding="utf-8",
    )

    subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        check=True,
    )

    report = tmp_path / "site" / "index.html"
    assert report.is_file()

    html = report.read_text(encoding="utf-8")
    assert "OrderLab Report" in html
    assert "35,000 KRW" in html
