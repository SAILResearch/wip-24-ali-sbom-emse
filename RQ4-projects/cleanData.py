import csv, pandas as pd

input_file = './data_files/duplicatesRemoved_GithubOutput.csv'
output_file = './data_files/clean_repoList.csv'

def read_file(filename):
    df = pd.read_csv(filename)
    return df

def cleanData():
    df = read_file(input_file)
    print(df.shape)
    count = 0
    df = df[~df.apply(lambda row: row['tool_used'] in row['repo_link'], axis=1)]
    df.to_csv(output_file, index=False) 

if __name__ == '__main__':
    cleanData()