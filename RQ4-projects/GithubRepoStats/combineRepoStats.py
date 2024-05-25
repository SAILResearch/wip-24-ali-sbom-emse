import random
import csv
import pandas as pd

spdx = f'..\csv_files\spdx_repoStats.csv'
cdx = f'..\csv_files\cyclonedx_randomSample_repos.csv'

output_file = f'..\csv_files\combined_repoStats.csv'


def readFile( fileName ):
    df = pd.read_csv( fileName )
    return df

def writeToCSV( df ):
    df.to_csv( output_file, index=False)

def combineRepoStats():
    df_spdx = readFile( spdx )
    df_cdx = readFile( cdx )
    df_spdx['format'] = 'spdx'
    df_cdx['format'] = 'cyclonedx'

    dfs = [df_spdx, df_cdx]
    df = pd.concat(dfs)
    writeToCSV( df )

if __name__ == "__main__":
    combineRepoStats()