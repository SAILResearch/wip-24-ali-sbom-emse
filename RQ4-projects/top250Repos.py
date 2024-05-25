import pandas as pd

format_type = 'CycloneDX'  # change the format type here (CycloneDX or SPDX)

input_file = f'./data_files/{format_type}_repoStats.csv'
output_file = f'./data_files/{format_type}_top250repoStatsTest.csv'

def readFile(fileName):
    df = pd.read_csv(fileName)
    return df

def getTopRepos():
    df = readFile(input_file)
    df = df.sort_values(by=['stars'], ascending=False).head(250)
    df.to_csv(output_file, index=False)

if __name__ =="__main__":
    getTopRepos()