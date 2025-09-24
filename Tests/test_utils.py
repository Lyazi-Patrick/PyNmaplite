import os
import json
import csv
import tempfile
from PyNmaplite.utils import save_to_csv, save_to_json

def test_save_to_json_and_csv(tmp_path):
    results = [{"port":22, "banner":"SSH-2.0-OpenSSH"},{"port":80,"banner":"HTTP/1.1 200 OK"}]
    json_file = tmp_path / "out.json"
    csv_file = tmp_path / "out.csv"

    save_to_json(results, str(json_file))
    assert json_file.exists()
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert data[0]["port"] == 22

    save_to_csv(results, str(csv_file))
    assert csv_file.exists()
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows[0]["port"] == "22"
    assert rows[1]["banner"] == "HTTP/1.1 200 OK"