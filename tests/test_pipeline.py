import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_recommendation_schema():
    records = json.loads((ROOT / "data" / "recommendations.json").read_text(encoding="utf-8"))
    required = {"name", "scientific_name", "crop", "prevent", "organic", "chemical", "field_note", "source"}
    assert "unknown" in records
    assert all(required.issubset(record) for record in records.values())


def test_production_assets_exist():
    assert (ROOT / "Dockerfile").exists()
    assert (ROOT / ".streamlit" / "config.toml").exists()
    assert (ROOT / "train.py").exists()
    assert (ROOT / "evaluate.py").exists()