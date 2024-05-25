import os, sys, getopt, math, json, requests, pandas as pd, glob, time, re
import urllib.parse
from linkheader_parser import parse
import xml.etree.ElementTree as ET
import pprint as pp

from github import Github

# Authentication is defined via github.Auth
from github import Auth

format_type = 'spdx'  # change the format type here (cyclonedx or spdx)

# personal access token
PAT = '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'
output_file = f'./data_files/RawGithubOutput.csv'
input_file = f'./data_files/SPDXnCDX_ToolsList.xlsx'

def dumpResponse(response):
    #data for debugging
    with open('rawResponse.json', "w") as outfile:
        txt = json.loads(response.text)
        json.dump(txt, outfile)
    print("JSON file printed to: rawResponse.json")

def dumpData(data,outputFile):
    #useful data as json
    with open(outputFile, "w") as outfile:
        json.dump(data, outfile)
    print("JSON file printed to: " + outputFile)

def readXLSX(input_file):
    data = pd.read_excel(input_file)
    return data

def addToCSV(data):
    file = open(output_file, 'w+')
    file.write("format,repo_link,tool_mention_link,tool_used,tool_link,search_key,language_filter\n")
    s = set() # to remove duplicates
    for results in data:
        for result in results:
            if result["repo"]+result['language'] not in s:
                file.write(f'{result["format"]},{result["repo"]},{result["tool_mention_link"]},{result["tool"]},{result["tool_link"]},"{result["search_key"]}",{result["language"]}\n')
                s.add( result["repo"]+result['language'] )

def runQuery(query):
    flag = 1
    sleep_time = 60
    while flag == 1:
        try:
            # Make the request using requests with authentication
            headers = {'Authorization': 'token ' + PAT}
            response = requests.request("GET", query, headers=headers)
            message = json.loads(response.text)['message']
        except (KeyError,TypeError) as e:
            return response
        if "exceeded" in message:
            print(f"Limit exceeded: Trying query again in {sleep_time} seconds ...")
            time.sleep(sleep_time)
            flag = 1
        else:
            flag = 0
    return response
    
def getNextQuery(response):
    # in case of pagination, we are trying to get the link for next page
    response.headers.setdefault('Link', 'no-link')
    nextLink = urllib.parse.unquote(response.headers['Link'])
    if nextLink != "no-link":
        result = parse(nextLink) # Parses header as JSON object
        # pp.pprint(result)
        try:
            return result['next']['url']
        except KeyError:
            return "no-link"
    return "no-link"

def processData( response, query ):
    try:
        repos = []
        responseJson = json.loads(response.text)
        # print(responseJson['total_count'], responseJson['incomplete_results'], len(responseJson['items']))
        for item in responseJson['items']:
            # pp.pprint(item) 
            repoLinks = {'repo':'N/A', 'tool_mention_link': 'N/A','search_key': 'N/A', 'language': 'N/A', 'tool':'N/A', 'format':'N/A', 'tool_link':'N/A'}
            repoLinks['repo'] = item['repository']['html_url']
            repoLinks['tool_mention_link'] = item['html_url']
            if item['repository']['fork']:
                print(item['html_url'])
            repos.append(repoLinks)
        return repos
    except:
        f1 = open("errorlog.txt","w+")
        f1.write(f"Error decoding JSON for search string: {query}\n")

# def getTimeRange(year, type, month=False, date=False):
#     '''
#     type:
#     1 - year range
#     2 - month range
#     3 - date range
#     '''
#     if type==3:
#         return f'{year}-{month}-{date}'
#     elif type==2:
#         return f'{year}-{month}-01..{year}-{month}-'

# def getDateRange(year, pattern):
#     '''
#     - first check for whole year, if yes then return range [startd_date..end_Date]
#     - else for each month, [st_m1..end_m1, st_m2..end_m2,...]
#     - else for each date, [st_d1..end_dn,...]
#     '''
#     start_date_year = f'{year}-01-01'
#     end_date_year = f'{year}-12-31'

languages = ['Makefile', 'C', 'TOML', 'Python', 'Nix', 'Java', 'Php', 'Ruby', 'Rust', 'Dart', 'Maven POM', 'Gradle', 'JSON', 'YAML', 'C++', 'Dockerfile', 'JavaScript', 'Shell', 'XML', 'C#', 'Groovy', 'Elixir', 'Erlang', 'TypeScript', 'Kotlin', 'Go', 'Alpine Abuild', 'SQL']

def queryGit(toolName, search_pattern, format, tool_link):
    pattern = search_pattern.replace("/",'%2F')
    pattern = pattern.replace(" ", "+")
    sboms = []
    for language in languages:
        language = language.replace(" ", "+")
        query = f'https://api.github.com/search/code?q="{pattern}"+language%3A{language}&per_page=100'
        print(query)
        while query != "no-link":
            response = runQuery(query)
            # print(response)
            if response.status_code == 422:
                break
            repos = processData( response, query )
            # print(len(repos))
            print(repos)

            for repo in repos:
                repo['search_key'] = toolName
                repo['language'] = language
                repo['tool'] = toolName
                repo['format'] = format
                repo['tool_link'] = tool_link
                sboms.append( repo )
                # print(len(sboms))
            query = getNextQuery(response)
    # print(sboms)
    return sboms

def run():
    data = readXLSX( input_file )
    # print(data.keys())
    results = []
    # print(data.values)
    for element in data.values:
        # print(element)
        format = element[0]
        tool_link = element[1]
        toolName = element[2]
        search_string = element[4]
        try:
            search_patterns = json.loads(search_string)
        except json.JSONDecodeError as e:
            f1 = open("errorlog.txt","a+")
            f1.write(f"Error decoding JSON for search string: {search_string}. Error: {str(e)}\n")
            continue  # Skip this iteration and move to the next element

        for search_pat in search_patterns:
            print(search_pat)
            result = queryGit(toolName, search_pat, format, tool_link)
            if result:
                results.append(result)
    addToCSV( results )

if __name__ == "__main__":
    outputFile = 'data.json'
    run()


