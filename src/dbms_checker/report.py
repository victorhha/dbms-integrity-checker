from __future__ import annotations
from typing import List
from .checks import Finding

def generate_markdown_report(findings: List[Finding]) -> str:
    lines = []
    lines.append("# DBMS Integrity Check Report\n")
    if not findings:
        lines.append("_No findings._\n")
        return "\n".join(lines)

    lines.append("| Level | Table | Message |")
    lines.append("|---|---|---|")
    for f in findings:
        lvl, tbl, msg = f.as_tuple()
        lines.append(f"| {lvl} | {tbl} | {msg} |")
    lines.append("")
    # Tiny legend
    lines.append("**Legend**: `ERROR` = failed integrity, `WARN` = possible issue/missing data, `INFO` = OK/pass.")
    lines.append("")
    return "\n".join(lines)
