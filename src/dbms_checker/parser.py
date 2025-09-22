from .model import Schema, Table, Column

def parse_schema_text(text: str) -> Schema:
    schema = Schema()
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]

    for line in lines:
        # Format: TableName(col1, col2, ...)
        if "(" not in line or not line.endswith(")"):
            raise ValueError(f"Bad table line: {line}")
        tname, inner = line.split("(", 1)
        tname = tname.strip()
        inner = inner[:-1]  # drop trailing ')'

        raw_cols = [c.strip() for c in inner.split(",")]
        table = Table(tname)

        for spec in raw_cols:
            if "(pk)" in spec:
                cname = spec.replace("(pk)", "").strip()
                table.columns[cname] = Column(name=cname, is_pk=True)
            elif "(fk:" in spec:
                cname, rhs = spec.split("(fk:", 1)
                cname = cname.strip()
                rhs = rhs.rstrip(")")
                if "." not in rhs:
                    raise ValueError(f"Bad fk spec: {spec}")
                rtable, rcol = rhs.split(".", 1)
                table.columns[cname] = Column(
                    name=cname,
                    fk_ref_table=rtable.strip(),
                    fk_ref_column=rcol.strip(),
                )
            else:
                table.columns[spec] = Column(name=spec)

        schema.add_table(table)

    return schema
