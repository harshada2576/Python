#!/usr/bin/env python3
"""
csv_to_sqlite.py
Simple CSV -> SQLite pipeline:
- reads CSV with pandas
- validates rows
- writes to SQLite using SQLAlchemy in chunks
"""

import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

CSV_PATH = "data/sample.csv"
SQLITE_DB = "sqlite:///data/mydb.sqlite"
TABLE_NAME = "users"
CHUNK_SIZE = 500  # rows per DB insert

# --- Sample schema creation (if needed) ---
def ensure_table(engine):
    metadata = MetaData()
    users = Table(
        TABLE_NAME, metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(200), nullable=False),
        Column("email", String(200), nullable=False, unique=False),
        Column("signup_ts", DateTime, nullable=True),
        Column("country", String(100), nullable=True),
    )
    metadata.create_all(engine)  # safe: creates only if not exists

# --- Basic validation function ---
def validate_row(row):
    # returns (is_valid, reason)
    if pd.isna(row.get("name")) or str(row["name"]).strip() == "":
        return False, "missing name"
    if pd.isna(row.get("email")) or "@" not in str(row["email"]):
        return False, "invalid email"
    return True, ""

def transform_row(row):
    # Example transforms: strip whitespace, normalize timestamp
    r = {
        "name": str(row["name"]).strip(),
        "email": str(row["email"]).strip().lower(),
        "country": str(row.get("country") or "").strip() or None
    }
    ts = row.get("signup_ts")
    try:
        if pd.isna(ts) or ts == "":
            r["signup_ts"] = None
        else:
            r["signup_ts"] = pd.to_datetime(ts)
    except Exception:
        r["signup_ts"] = None
    return r

def load_csv_to_db(csv_path, engine_url):
    engine = create_engine(engine_url, echo=False)
    ensure_table(engine)

    # use pandas to read in chunks if file is big
    total = 0
    inserted = 0
    bad = 0
    bad_rows = []

    for chunk in pd.read_csv(csv_path, chunksize=CHUNK_SIZE):
        batch = []
        for _, row in chunk.iterrows():
            total += 1
            valid, reason = validate_row(row)
            if not valid:
                bad += 1
                bad_rows.append((total, reason, row.to_dict()))
                continue
            batch.append(transform_row(row))

        if not batch:
            continue

        df_batch = pd.DataFrame(batch)
        try:
            # use to_sql with SQLAlchemy engine; if table exists, append
            df_batch.to_sql(TABLE_NAME, engine, if_exists="append", index=False, method="multi", chunksize=CHUNK_SIZE)
            inserted += len(df_batch)
        except SQLAlchemyError as e:
            # fallback: use smaller chunks or log and continue
            print("DB error inserting chunk:", e)
            bad += len(df_batch)
            # optionally write failing chunk to file / topic

    print(f"Total rows read: {total}. Inserted: {inserted}. Invalid: {bad}")
    if bad_rows:
        print("Example invalid rows:", bad_rows[:3])

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    # create a small sample CSV if not present
    if not os.path.exists(CSV_PATH):
        sample = """id,name,email,signup_ts,country
1,Alice,alice@example.com,2025-01-05 10:00:00,India
2,Bob,bob-at-example.com,2025-02-10 12:30:00,US
3, ,charlie@example.com,,
4,Eve,eve@example.com,2025-03-01,UK
"""
        with open(CSV_PATH, "w") as f:
            f.write(sample)
        print("Wrote sample CSV to", CSV_PATH)

    load_csv_to_db(CSV_PATH, SQLITE_DB)
