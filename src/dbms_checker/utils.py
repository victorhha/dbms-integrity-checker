from __future__ import annotations
import csv
import os
from typing import Dict, List, Optional

def load_csv_table(csv_dir: Optional[str], table_name: str) -> Optional[List[Dict[str, str]]]:
    """Return list of rows (dicts) from csv_dir/TableName.csv, or None if not found/disabled."""
    if not csv_dir:
        return None
    path = os.path.join(csv_dir, f"{table_name}.csv")
    if not os.path.exists(path):
        return None
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [ {k: (v if v is not None else "") for k, v in row.items()} for row in reader ]

def is_null(v: str) -> bool:
    return v is None or str(v).strip() == ""
