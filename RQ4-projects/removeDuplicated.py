import csv
import pandas as pd

input_file = './data_files/RawGithubOutput.csv'
output_file = './data_files/duplicatesRemoved_GithubOutput.csv'

def readFile( fileName ):
    df = pd.read_csv(fileName)
    return df

def removeDuplicates():
    df = readFile( input_file ) 
    s = set()
    indices_to_remove = []
    for idx, row in df.iterrows():
        if row['repo_link'] in s:
            indices_to_remove.append(idx)
        else:
            s.add(row['repo_link'])
    print(indices_to_remove)
    df = df.drop(indices_to_remove)
    
    df.to_csv(output_file, index=False)
    
if __name__ == "__main__":
    removeDuplicates()