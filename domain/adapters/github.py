from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta
import time
import os
from crawler.domain.repo import Repository

class GitHubAdapter:
    def __init__(self):
        transport = RequestsHTTPTransport(
            url="https://api.github.com/graphql",
            headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
            use_json=True,
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def fetch_repos(self, target_count=100_000):
        repos = []
        query_str = "stars:>0"  # any repo with at least 1 star
        after = None
        page = 0

        while len(repos) < target_count:
            page += 1
            variables = {
                "query": query_str,
                "first": min(100, target_count - len(repos)),
                "after": after
            }
            query = gql("""
            query($query: String!, $first: Int!, $after: String) {
                search(type: REPOSITORY, query: $query, first: $first, after: $after) {
                    nodes {
                        ... on Repository {
                            nameWithOwner
                            stargazerCount
                        }
                    }
                    pageInfo { endCursor hasNextPage }
                }
                rateLimit { remaining cost resetAt }
            }
            """)

            print(f"Page {page} | Fetched {len(repos)} so far...")
            result = self.client.execute(query, variable_values=variables)
            
            for node in result['search']['nodes']:
                repos.append(Repository(
                    full_name=node['nameWithOwner'],
                    stars=node['stargazerCount']
                ))
                if len(repos) >= target_count:
                    break

            page_info = result['search']['pageInfo']
            after = page_info['endCursor']
            if not page_info['hasNextPage']:
                print("No more pages!")
                break

            # Respect rate limit
            remaining = result['rateLimit']['remaining']
            if remaining < 10:
                print("Rate limit low, sleeping 60s...")
                time.sleep(60)

            time.sleep(0.8)  # Be gentle

        return repos[:target_count]