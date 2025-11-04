from sqlalchemy import create_engine, text
from crawler.domain.repo import Repository

class PostgresAdapter:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def upsert_repo(self, repo: Repository):
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO repositories (full_name, stars, last_crawled)
                VALUES (:full_name, :stars, COALESCE(:crawled_at, NOW()))
                ON CONFLICT (full_name) 
                DO UPDATE SET stars = EXCLUDED.stars, last_crawled = NOW()
            """), {
                "full_name": repo.full_name,
                "stars": repo.stars,
                "crawled_at": repo.crawled_at
            })
            conn.commit()