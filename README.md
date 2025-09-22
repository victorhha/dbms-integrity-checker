# 🗄️ DBMS Integrity Checker

A lightweight **Database Management System (DBMS) Integrity Checker** built in Python.  
It parses simple schema definitions, validates primary & foreign key constraints, and generates audit reports in Markdown format.  

---

## 🚀 Features
- Parse schema DSL like:

  ```
  T1(k1(pk), k2(fk:T2.k2), A, B)
  T2(k2(pk), k3(fk:T3.k3), C)
  T3(k3(pk), D)
  ```

- Extract **primary keys**, **foreign keys**, and non-key columns.  
- Validate:
  - Primary key uniqueness  
  - Referential integrity (foreign keys → referenced table)  
- Generate a clean **Markdown report** of findings.  
- Works with example CSV data for hands-on testing.  

---

## 📂 Project Structure
```
dbms-integrity-checker/
├── README.md
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── examples/
│   ├── schema.txt
│   └── data/
│       ├── T1.csv
│       ├── T2.csv
│       └── T3.csv
└── src/
    └── dbms_checker/
        ├── __init__.py
        ├── cli.py
        ├── model.py
        ├── parser.py
        ├── utils.py
        ├── checks.py
        └── report.py
```

---

## ⚙️ Installation
Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/victorhha/dbms-integrity-checker.git
cd dbms-integrity-checker

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

---

## ▶️ Usage

### Schema-only analysis
```bash
python -m src.dbms_checker.cli --schema examples/schema.txt
```

### With CSV data + Markdown report
```bash
python -m src.dbms_checker.cli     --schema examples/schema.txt     --csv-dir examples/data     --out report.md
```

This produces a `report.md` like:

| Level | Table | Message |
|-------|-------|---------|
| INFO  | T1    | PK uniqueness OK (3 rows) |
| INFO  | T1    | FK T1.k2 OK |
| INFO  | T2    | PK uniqueness OK (2 rows) |
| INFO  | T2    | FK T2.k3 OK |
| INFO  | T3    | PK uniqueness OK (2 rows) |

---

## 🧪 Example Data
- `examples/schema.txt` → defines the schema (T1, T2, T3).  
- `examples/data/` → contains CSVs with valid sample data.  

---

## 📜 Roadmap
- Add **normalization checks** (1NF, 2NF, 3NF heuristics).  
- Add **unit tests** (`pytest`).  
- Add GitHub Actions for CI/CD.  

---

## 📄 License
MIT License © 2025 Victor Ha
