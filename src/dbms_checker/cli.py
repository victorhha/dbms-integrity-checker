import argparse
from .parser import parse_schema_text

def main():
    ap = argparse.ArgumentParser(description="DBMS Integrity Checker (minimal)")
    ap.add_argument("--schema", required=True, help="Path to schema.txt")
    args = ap.parse_args()

    with open(args.schema, "r", encoding="utf-8") as f:
        schema_text = f.read()

    schema = parse_schema_text(schema_text)

    print("✅ Parsed schema successfully!")
    for table in schema.tables.values():
        print(f"Table: {table.name}")
        print(f"  PK: {table.pk_columns()}")
        for fk in table.fks():
            print(f"  FK: {fk.column} -> {fk.ref_table}.{fk.ref_column}")

if __name__ == "__main__":
    main()
