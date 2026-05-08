from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

from core.models import AuditRecord


class AuditLogger:
    def __init__(self, data_dir: str | None = None) -> None:
        root = data_dir or os.getenv("IMMUNE_CRYSTAL_DATA", "data")
        self.path = Path(root) / "audit.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self._init()

    def write(self, record: AuditRecord) -> AuditRecord:
        self.conn.execute(
            "insert into audit(id,event,query,answer,purity_score,lineage,metadata,created_at) values(?,?,?,?,?,?,?,?)",
            (
                record.id,
                record.event,
                record.query,
                record.answer,
                record.purity_score,
                json.dumps([item.model_dump() for item in record.lineage], ensure_ascii=False),
                json.dumps(record.metadata, ensure_ascii=False),
                record.created_at,
            ),
        )
        self.conn.commit()
        return record

    def get(self, audit_id: str) -> AuditRecord | None:
        row = self.conn.execute("select * from audit where id=?", (audit_id,)).fetchone()
        if not row:
            return None
        return self._row_to_record(row)

    def list(self, limit: int = 50) -> list[AuditRecord]:
        rows = self.conn.execute("select * from audit order by created_at desc limit ?", (limit,)).fetchall()
        return [self._row_to_record(row) for row in rows]

    def _init(self) -> None:
        self.conn.execute("pragma journal_mode=wal")
        self.conn.execute("pragma synchronous=normal")
        self.conn.execute(
            """
            create table if not exists audit(
                id text primary key,
                event text not null,
                query text,
                answer text,
                purity_score real,
                lineage text not null,
                metadata text not null,
                created_at real not null
            )
            """
        )
        self.conn.commit()

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

    def __del__(self) -> None:
        self.close()

    @staticmethod
    def _row_to_record(row: tuple) -> AuditRecord:
        return AuditRecord(
            id=row[0],
            event=row[1],
            query=row[2],
            answer=row[3],
            purity_score=row[4],
            lineage=json.loads(row[5]),
            metadata=json.loads(row[6]),
            created_at=row[7],
        )
