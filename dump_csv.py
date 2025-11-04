import os
import csv
from sqlalchemy import create_engine, text

DB_URL = "postgresql+pg8000://postgres:postgres@localhost:5432/postgres"

def export_to_csv():
    engine = create_engine(DB_URL)
    query = text("SELECT full_name, stars, last_crawled FROM repositories ORDER BY stars DESC")
    
    with engine.connect() as conn:
        rows = conn.execute(query).fetchall()

    with open("repos.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["full_name", "stars", "crawled_at"])
        writer.writerows(rows)

    print(f"Dumped {len(rows):,} rows → repos.csv")

if __name__ == "__main__":
    export_to_csv()