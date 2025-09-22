from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class Column:
    name: str
    is_pk: bool = False
    fk_ref_table: Optional[str] = None
    fk_ref_column: Optional[str] = None

    @property
    def is_fk(self) -> bool:
        return self.fk_ref_table is not None and self.fk_ref_column is not None

@dataclass
class ForeignKey:
    table: str
    column: str
    ref_table: str
    ref_column: str

@dataclass
class Table:
    name: str
    columns: Dict[str, Column] = field(default_factory=dict)

    def pk_columns(self) -> List[str]:
        return [c.name for c in self.columns.values() if c.is_pk]

    def fks(self) -> List[ForeignKey]:
        return [
            ForeignKey(self.name, c.name, c.fk_ref_table, c.fk_ref_column)
            for c in self.columns.values()
            if c.is_fk
        ]

@dataclass
class Schema:
    tables: Dict[str, Table] = field(default_factory=dict)

    def add_table(self, table: Table) -> None:
        self.tables[table.name] = table
