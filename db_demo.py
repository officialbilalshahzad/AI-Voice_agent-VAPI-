from __future__ import annotations
from sqlalchemy import text

from database import engine #, init_db

def run_sql(query: str):
    with engine.begin() as conn:
        result = conn.execute(text(query))
        return result.fetchall() if result.returns_rows else result.rowcount
    
#query = """Insert into appointments (patient_name, reason, start_time) values ('John Doe', 'Checkup', '2024-07-01 10:00:00')"""
query = """Select * from appointments"""
print(run_sql(query))