import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from crawler.adapters.github import GitHubAdapter
from crawler.adapters.postgres import PostgresAdapter

def main():
    db_url = "postgresql+pg8000://postgres:postgres@localhost:5432/postgres"
    db = PostgresAdapter(db_url)

    github = GitHubAdapter()
    repos = github.fetch_repos(100_000)

    print(f"Saving {len(repos):,} repos...")
    for i, repo in enumerate(repos):
        db.upsert_repo(repo)
        if i % 1000 == 0:
            print(f"   → Saved {i:,} repos")

    print("DONE! 100,000 repos saved.")

if __name__ == "__main__":
    main()