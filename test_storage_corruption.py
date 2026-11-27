from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from storage import load_log


def test_malformed_json_line_reports_its_line_number():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "events.jsonl"
        path.write_text("not-json\\n", encoding="utf-8")

        with pytest.raises(ValueError, match="invalid log at line 1"):
            load_log(path)
