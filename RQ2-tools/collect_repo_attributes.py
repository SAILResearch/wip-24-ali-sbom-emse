import csv
import time

import requests
import random
from datetime import datetime, timezone


def get_commits_count(repo_url):
    # Extract username and repository name from the URL
    username, repo_name = repo_url.split('/')[-2:]

    # Make a request to the GitHub API to get commits
    commits_count = 0
    page = 1
    per_page = 100  # Maximum number of commits per page
    while True:
        url = f"https://api.github.com/repos/{username}/{repo_name}/commits?page={page}&per_page={per_page}"
        headers = {"Accept": "application/vnd.github.v3+json",
                   "Authorization": f"Token {'YourToken'}"}
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            commits = response.json()

            # Check if there are no more commits
            if len(commits) == 0:
                break

            # Increment the commits count
            commits_count += len(commits)

            # Move to the next page
            page += 1
        else:
            # Print an error message if the request failed
            print(f"Failed to fetch commits for {repo_url}. Status code: {response.status_code}")
            return None

    return commits_count


def get_pulls_count(repo_url, state):
    # Extract username and repository name from the URL
    username, repo_name = repo_url.split('/')[-2:]

    # Make a request to the GitHub API to get commits
    pulls_count = 0
    page = 1
    per_page = 100  # Maximum number of commits per page
    while True:
        url = f"https://api.github.com/repos/{username}/{repo_name}/pulls?state={state}&page={page}&per_page={per_page}"
        headers = {"Accept": "application/vnd.github.v3+json",
                   "Authorization": f"Token {'YourToken'}"}
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            pulls = response.json()

            # Check if there are no more commits
            if len(pulls) == 0:
                break

            # Increment the commits count
            pulls_count += len(pulls)

            # Move to the next page
            page += 1
        else:
            # Print an error message if the request failed
            print(f"Failed to fetch commits for {repo_url}. Status code: {response.status_code}")
            return None

    return pulls_count


def get_repo_creation_date(repo_url):
    # Extract username and repository name from the URL
    username, repo_name = repo_url.split('/')[-2:]

    # Make a request to the GitHub API to get repository information
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"Token {'YourToken'}"}
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON and return the creation date
        repo_info = response.json()
        creation_date = repo_info['created_at']
        return creation_date
    else:
        # Print an error message if the request failed
        print(f"Failed to fetch repository creation date for {repo_url}. Status code: {response.status_code}")
        return None


def calculate_repo_age(creation_date):
    # Convert creation date string to datetime object
    creation_datetime = datetime.fromisoformat(creation_date.replace('Z', '+00:00'))

    # Format the creation date to year-month-day
    formatted_creation_date = creation_datetime.strftime('%Y-%m-%d')

    # Get today's date
    today = datetime.utcnow().replace(tzinfo=timezone.utc)

    # Calculate the age of the repository in days
    repo_age_days = (today - creation_datetime).days
    return formatted_creation_date, repo_age_days


def get_releases_count(repo_url):
    # Extract username and repository name from the URL
    username, repo_name = repo_url.split('/')[-2:]

    # Make a request to the GitHub API to get repository information
    url = f"https://api.github.com/repos/{username}/{repo_name}/releases"
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"Token {'YourToken'}"}
    params = {'per_page': 100, 'page': 1}
    total_releases = 0
    while True:
        releases_response = requests.get(url, headers=headers, params=params)

        if releases_response.status_code == 200:
            releases_info = releases_response.json()
            total_releases += len(releases_info)

            if 'Link' in releases_response.headers and 'rel="next"' in releases_response.headers['Link']:
                params['page'] += 1
            else:
                break
        else:
            print(f"Failed to fetch releases information for {repo_url}. Status code: {releases_response.status_code}")
            break

    return total_releases


def get_stars_and_watchers_count(repo_url):
    # Extract username and repository name from the URL
    username, repo_name = repo_url.split('/')[-2:]

    # Make a request to the GitHub API to get contributors
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"Token {'YourToken'}"}
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON and return the number of contributors
        repo_info = response.json()
        stars_count = repo_info['stargazers_count']
        watchers_count = repo_info['subscribers_count']
        return stars_count, watchers_count
    else:
        # Print an error message if the request failed
        print(f"Failed to fetch contributors count for {repo_url}. Status code: {response.status_code}")
        return None, None


def update_csv(input_file_path, output_file_path, start_row=1):
    # Open the input CSV file and create a new CSV file for writing
    with open(input_file_path, 'r', newline='') as csvfile, open(output_file_path, 'w', newline='') as output_csv:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        # Write header if the starting row is 1, otherwise, copy the header from the input file
        writer.writeheader()

        # Set API wait time
        sleep_time = random.randint(10, 30)

        # Skip rows until the starting row
        for _ in range(start_row - 1):
            next(reader)

        # Iterate over each row in the input CSV file
        for row in reader:
            repo_url = row['link']

            # Get the total number of commits of each repo
            commits_count = get_commits_count(repo_url)

            # Get the number of open PRs and closed PRs of each repo
            open_pulls_count = get_pulls_count(repo_url, 'open')
            closed_pulls_count = get_pulls_count(repo_url, 'closed')

            # Get the age of each repo
            creation_date = get_repo_creation_date(repo_url)
            # Calculate the age of the repository
            if creation_date:
                formatted_creation_date, repo_age_days = calculate_repo_age(creation_date)
            else:
                formatted_creation_date, repo_age_days = 'Error', 'Error'

            # Get the total number of releases of each repo
            releases_count = get_releases_count(repo_url)

            # Get the number of starts and watchers of each repo
            stars_count, watchers_count = get_stars_and_watchers_count(repo_url)

            # Update the row with the number of commits and write it to the output CSV file
            row['Commits'] = commits_count if commits_count is not None else 'Error'
            row['Open Pull Requests'] = open_pulls_count if open_pulls_count is not None else 'Error'
            row['Closed Pull Requests'] = closed_pulls_count if closed_pulls_count is not None else 'Error'
            row['Creation Time'] = formatted_creation_date
            row['Age (Days)'] = repo_age_days
            row['Releases'] = releases_count
            row['Stars'] = stars_count if stars_count is not None else 'Error'
            row['Watchers'] = watchers_count if watchers_count is not None else 'Error'
            writer.writerow(row)

            # Add a delay between API requests to avoid sending too many requests too quickly
            time.sleep(sleep_time)


if __name__ == "__main__":
    # Replace 'input.csv' and 'output.csv' with your input and output file paths
    input_file = 'input.csv'
    output_file = 'output.csv'
    update_csv(input_file, output_file, 1)
