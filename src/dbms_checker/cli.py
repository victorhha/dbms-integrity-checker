import argparse
from .parser import parse_schema_text
from .checks import run_checks
from .report import generate_markdown_report

def main():
    ap = argparse.ArgumentParser(description="DBMS Integrity Checker")
    ap.add_argument("--schema", required=True, help="Path to schema.txt")
    ap.add_argument("--csv-dir", help="Directory containing TableName.csv files (optional)")
    ap.add_argument("--out", help="Write Markdown report to this file (optional)")
    args = ap.parse_args()

    # Parse schema
    with open(args.schema, "r", encoding="utf-8") as f:
        schema_text = f.read()
    schema = parse_schema_text(schema_text)

    # Basic echo
    print("✅ Parsed schema successfully!")
    for table in schema.tables.values():
        print(f"Table: {table.name}")
        print(f"  PK: {table.pk_columns()}")
        for fk in table.fks():
            print(f"  FK: {fk.column} -> {fk.ref_table}.{fk.ref_column}")

    # Run data checks if csv-dir provided
    findings = run_checks(schema, args.csv_dir)

    # Output report
    md = generate_markdown_report(findings)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"\n📝 Report written to {args.out}")
    else:
        print("\n" + md)

if __name__ == "__main__":
    main()
