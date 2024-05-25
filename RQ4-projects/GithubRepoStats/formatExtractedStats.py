from math import nan
import pandas as pd

format_type = 'SPDX'  # change the format type here (CycloneDX or SPDX)
input_file = f'..\data_files\{format_type}_top250repoStats.csv'
output_file = f'..\data_files\{format_type}_formattedStats.csv'

def readFile( fileName ):
    df = pd.read_csv( fileName )
    return df

def expandData( data, key ):
    df = pd.DataFrame(columns=['format','attribute','count'])
    df['count'] = data[key]
    df['format'] = format_type
    df['attribute'] = key
    indices = []
    list = pd.isna(df['count'])
    for idx,val in enumerate(list):
        if val:
            indices.append( idx )
    return df.drop(indices)

def formatStats():
    data = readFile( input_file )
    headers = ['stars',
               'watchers',
               'forks',
               'releases',
               'usedBy',
               'contributors',
               'openIssues',
               'closedIssues',
               'openPRs',
               'closedPRs',
               'commits', 
               'programmingLanguage']
    
    result = pd.DataFrame(columns=['format','attribute','count'])
    for key in headers:
        df = expandData( data, key )
        result = pd.concat([result, df],
                  ignore_index = True)
    for idx,row in result.iterrows():
        if row['attribute'] != 'programmingLanguage':
            if type(row['count']) == str:
                if ',' in row['count']:
                    result.at[idx, 'count'] = row['count'].replace(',', '')
    result.to_csv( output_file, index=False )

if __name__ == "__main__":
    formatStats()
    

