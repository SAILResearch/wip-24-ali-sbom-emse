import pandas as pd
import re
import requests
from collections import defaultdict
import argparse
import pickle

# Set up argument parser
parser = argparse.ArgumentParser(description='Fetch and process commit data from GitHub repositories.')
parser.add_argument('token', type=str, help='GitHub personal access token')
parser.add_argument('csv_file', type=str, help='Path to the CSV file containing repository data')

args = parser.parse_args()

# Use the provided arguments
GITHUB_TOKEN = args.token
file_path = args.csv_file

# Load the CSV file
df = pd.read_csv(file_path)

# Extract repository owner and name from the URL
def extract_repo_info(url):
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if match:
        return match.groups()
    return None, None

df['repo_owner'], df['repo_name'] = zip(*df['link'].apply(extract_repo_info))

headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Function to fetch commits for a repository
def fetch_commits(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    commits = []
    page = 1
    while True:
        response = requests.get(url, headers=headers, params={'per_page': 100, 'page': page})
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        commits.extend(data)
        page += 1
    return commits

# Function to get commit counts per contributor
def get_commit_counts(owner, repo):
    commits = fetch_commits(owner, repo)
    commit_counts = defaultdict(int)
    for commit in commits:
        if 'author' in commit and commit['author']:
            author = commit['author']['login']
            commit_counts[author] += 1
    return commit_counts

# Get commit counts for each repository
all_commit_counts = defaultdict(int)
for _, row in df.iterrows():
    owner, repo = row['repo_owner'], row['repo_name']
    print(f'Processing repository: {owner}/{repo}')
    if owner and repo:
        commit_counts = get_commit_counts(owner, repo)
        for contributor, count in commit_counts.items():
            all_commit_counts[contributor] += count

# Sort the dictionary by commit number
sorted_commit_counts = dict(sorted(all_commit_counts.items(), key=lambda item: item[1], reverse=True))

# Save the dictionary to a pickle file
with open('commit_counts.pkl', 'wb') as f:
    pickle.dump(sorted_commit_counts, f)
