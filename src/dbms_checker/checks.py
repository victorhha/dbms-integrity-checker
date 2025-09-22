from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
from .model import Schema, Table
from .utils import load_csv_table, is_null

class Finding:
    # level: INFO | WARN | ERROR | SUGGESTION
    def __init__(self, level: str, message: str, table: Optional[str] = None):
        self.level = level
        self.message = message
        self.table = table

    def as_tuple(self) -> Tuple[str, str, str]:
        return (self.level, self.table or "-", self.message)

def _check_pk_uniqueness(table: Table, rows: List[Dict[str, str]]) -> List[Finding]:
    out: List[Finding] = []
    pk = table.pk_columns()
    if not pk:
        out.append(Finding("WARN", f"No primary key defined for {table.name}", table.name))
        return out

    seen: Set[Tuple[str, ...]] = set()
    for i, r in enumerate(rows, start=1):
        key = tuple(r.get(col, "") for col in pk)
        if any(is_null(v) for v in key):
            out.append(Finding("ERROR", f"Null in PK at row {i}: {key}", table.name))
            continue
        if key in seen:
            out.append(Finding("ERROR", f"Duplicate PK at row {i}: {key}", table.name))
        else:
            seen.add(key)
    if not any(f.level == "ERROR" for f in out):
        out.append(Finding("INFO", f"PK uniqueness OK ({len(rows)} rows)", table.name))
    return out

def _build_ref_cache(schema: Schema, csv_dir: Optional[str]) -> Dict[str, Set[str]]:
    """Map 'Table.col' -> set of accepted values (from referenced table)."""
    cache: Dict[str, Set[str]] = {}
    if not csv_dir:
        return cache
    for t in schema.tables.values():
        rows = load_csv_table(csv_dir, t.name) or []
        for col in t.columns.values():
            key = f"{t.name}.{col.name}"
            cache[key] = set()
            for r in rows:
                v = r.get(col.name, "")
                if not is_null(v):
                    cache[key].add(v)
    return cache

def _check_fk_integrity(schema: Schema, table: Table, rows: List[Dict[str, str]], ref_cache: Dict[str, Set[str]]) -> List[Finding]:
    out: List[Finding] = []
    for fk in table.fks():
        ref_key = f"{fk.ref_table}.{fk.ref_column}"
        ref_vals = ref_cache.get(ref_key, set())
        missing = 0
        for r in rows:
            v = r.get(fk.column, "")
            if is_null(v):
                continue  # nullable FK allowed in this minimal checker
            if v not in ref_vals:
                missing += 1
        if missing:
            out.append(Finding("ERROR", f"FK {table.name}.{fk.column} → {fk.ref_table}.{fk.ref_column}: {missing} missing refs", table.name))
        else:
            out.append(Finding("INFO", f"FK {table.name}.{fk.column} OK", table.name))
    return out

def run_checks(schema: Schema, csv_dir: Optional[str]) -> List[Finding]:
    findings: List[Finding] = []

    # Preload reference cache for FK validation
    ref_cache = _build_ref_cache(schema, csv_dir)

    for t in schema.tables.values():
        rows = load_csv_table(csv_dir, t.name)
        if rows is None:
            findings.append(Finding("WARN", f"No CSV found for table {t.name}; data checks skipped", t.name))
            continue

        # PK uniqueness
        findings.extend(_check_pk_uniqueness(t, rows))
        # FK existence
        findings.extend(_check_fk_integrity(schema, t, rows, ref_cache))

    return findings
