This readme files provides the description of the content in each files
- RawGithubOutput.csv: (3944 lines)
        - contains the output of (searchGithub.py)
        - contains the repositories that are potentially generating the SBOMs
        - this is uncleaned data (needed to remove duplicates and tools)

- duplicatesRemoved_GithubOutput.csv: (2524 lines)
        - output after removing the duplicates repos from the above file
        
- clean_repoList.csv: (2426 lines)
        - contains clean data after removing the repos that were the actual tool repos.
        - like removing the https:github.com/cyclonedx/codegen which is the tool repo for codegen

- SPDXnCDX_ToolsList.xlsx: (65 lines)
        - contains the list of the tools that are mentioned in the official websites of spdx and cyclonedx
        - we are only using the tools whose code is freely available on the github and are used for "generation" of SBOMs



# other stats:
Only SPDX: 307
Only cyclonedx: 1087
Both SPDX and CycloneDX: 1032
Total: 2426 (same as clean_repoList.csv)