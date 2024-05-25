from importlib.resources import open_binary
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pprint as pp
import csv

format_type = 'SPDX'  # change the format type here (CycloneDX or SPDX)
input_file = f'..\data_files\{format_type}_repos.csv'
output_file = f'..\data_files\{format_type}_repoStats.csv'

def getNumericalValue( text ):
    numValue = ""
    for element in text:
        if element != '.' and element != 'k' and element != ',':
            numValue += element
    if text[-1] == 'k':
        numValue += "000"
    return numValue

def getGithubProperties(URL):
    # URL = "https://github.com/<user-name>/<repo-name>"
    page = requests.get(URL)

    if not page:
        f1 = open("errorlog.txt","a+")
        f1.write(f'Error in link: {URL}\n')
        return None

    property = {
        'tool_used': None,
        'about': None,
        'link': None,
        'projectCategory': [],
        'tags': None,
        'licence': None,
        'stars': None,
        'watchers': None,
        'forks': None,
        'releases': None,
        'latestRelease': None,
        'packages': None,
        'usedBy': None,
        'contributors': None,
        'openIssues' : None,
        'closedIssues' : None,
        'openPRs' : None,
        'closedPRs' : None,
        'commits': None,
        "programmingLanguage": None
    }
        
    soup = BeautifulSoup(page.content, "html.parser")
    pageheadActions = soup.find("div", class_="BorderGrid-cell")

    # links
    link = pageheadActions.find("a", href=True)
    property["link"] = link['href']

    # topics
    topics_html = pageheadActions.find_all("a", class_="topic-tag")
    topics = []
    for topic in topics_html:
        topics.append(topic.text.strip())
    property["tags"] = topics

    # about
    about = pageheadActions.find("p")
    if about is not None:
        property['about'] = about.text.strip()

    # licence, stars, watchers, forks
    allA_linkmuted = pageheadActions.find_all("a", class_="Link--muted", href=True)
    for a in allA_linkmuted:
        href = a['href']
        text = a.text.strip()
        if text:
            text = text.split('\n')
        else:
            continue
        n = href.split('/')[-1]
        if n == "LICENSE":
            property['licence'] = text[0].strip()
        if n == "stargazers":
            property['stars'] = getNumericalValue( text[0].strip() )
        if n == "watchers":
            property['watchers'] = getNumericalValue( text[0].strip() )
        if n == "forks":
            property['forks'] = getNumericalValue( text[0].strip() )

    # releases, latestReleases, contributors, usedBy, packages
    layout_sidebar = soup.find("div", class_="Layout-sidebar")
    allA_linkprimary = layout_sidebar.find_all("a", class_="Link--primary", href=True)
    for a in allA_linkprimary:
        text = a.text.strip()
        if text:
            text = text.split('\n')
        else:
            continue
        href = a['href']
        n = href.split('/')[-1]
        if n == "releases" and len(text)>1:
            property['releases'] = getNumericalValue( text[1].strip() )

        n1 = href.split('/')[-2]
        if n1 == "tag":
            property['latestRelease'] = text[0].strip()

        n2 = href.split('/')[-1]
        if n2 == "contributors" and len(text)>1:
            property['contributors'] = getNumericalValue( text[1].strip() )

        n3 = href.split('/')[-1]
        if "packages?" in n3 and len(text)>1:
            property['packages'] = getNumericalValue( text[1].strip() )
        n4 = href.split('/')[-1]
        if n4 == "dependents":
            property['usedBy'] = getNumericalValue( text[0].split(" ")[-1] )

    commitsBox = soup.find_all("a", class_="pl-3 pr-3 py-3 p-md-0 mt-n3 mb-n3 mr-n3 m-md-0 Link--primary no-underline no-wrap")
    property['commits'] = commitsBox[0].strong.string

    languages = soup.find_all("span", class_="Progress-item color-bg-success-emphasis", itemprop="keywords")
    if len(languages)>0:
        language = languages[0]['aria-label'].split(" ")
        property['programmingLanguage'] = language[0]

    return property


def getIssues(URL):
    # URL = "https://github.com/<user-name>/<repo-name>/issues"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    head = soup.find("div", class_="table-list-header-toggle states flex-auto pl-0")
    allAs = head.find_all("a", class_="btn-link", href=True)
    openIssues = getNumericalValue( allAs[0].text.strip().split(" ")[0] )
    closedIssues = getNumericalValue( allAs[1].text.strip().split(" ")[0] ) 

    return openIssues, closedIssues

def getPRs(URL):
    # URL = "https://github.com/<user-name>/<repo-name>/pulls"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    head = soup.find("div", class_="table-list-header-toggle states flex-auto pl-0")
    allAs = head.find_all("a", class_="btn-link", href=True)
    openPRs = getNumericalValue( allAs[0].text.strip().split(" ")[0] )
    closedPRs = getNumericalValue( allAs[1].text.strip().split(" ")[0] )

    return openPRs, closedPRs

def getRepoStats( url ):
    print(url)
    property = getGithubProperties(url)
    if property:
        property['openIssues'], property['closedIssues'] = getIssues(url + "/issues")
        property['openPRs'], property['closedPRs'] = getPRs(url + "/pulls")
    # pp.pprint( property )
    return property

def readData():
    data = []
    with open(input_file, 'r') as file:
        file.seek(0)
        csv_reader = csv.reader(file)
        if next( csv_reader, None )==None:
            return data
        for row in csv_reader:
            data.append(row)
    return data

def writeToCSV( data ):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

def getAllRepoStats():
    data = readData()
    properties = []
    linkSet = set()
    count = 0
    for item in data:
        link = item[1]
        tool = item[3]
        # for link in links.split("'"):
        #     link = link.strip()
        #     if len(link)>1 and link not in linkSet:
        #         # print(link)
        #         linkSet.add(link)
        property = getRepoStats( link )
        if property:
            count += 1
            property['link'] = link
            property['tool_used'] = tool
            properties.append( property )
    print(count)
    writeToCSV( properties )

if __name__ == "__main__":
    getAllRepoStats()