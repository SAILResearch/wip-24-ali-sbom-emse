from time import sleep
import pandas as pd
import requests
import json
import csv

format_type = 'SPDX'  # change the format type here (CycloneDX or spdx)
input_file = f'E:\MITACS\intern-23-arshdeep\RQ2-Projects\data_files\{format_type}_RepoLinks.csv'
output_file = f'{format_type}_dateCreated.csv'
error_file = f'dump.txt'
PAT = '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'

def modifyURL(url=None):
    try:
        if url is None:
            raise ValueError("Input url cannot be None.")
        url = url.replace("github.com", "api.github.com/repos")
        return url
    except ValueError as e:
        print("Error:", e)

def getCreationDate(url = None):
    url = modifyURL(url)
    date = None
    headers = {'Authorization': 'token ' + PAT}
    r = requests.request("GET", url, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        txt = json.loads(r.text)
        date = txt['created_at'][:10]
        print(url, date)
    else:
        print(url, "not loaded")
        f = open(error_file, "a+")
        f.write(url)
        sleep(20)
    return date

def run():
    df = pd.read_csv(input_file)
    # print(df)
    dateCreated = []
    for url in df['links']:
        # print(url)
        date = getCreationDate(url)
        # print(date)
        dateCreated.append(date)
    dateCreationDf = pd.DataFrame(dateCreated, columns=['createdDate'])
    # print(dateCreationDf)
    dateCreationDf.to_csv(output_file, index=False)



if __name__ == "__main__":
    run()