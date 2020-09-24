#!/bin/bash
## filename: fetch_repo_branches.sh

repository_list=(
AGE2E-Core-Base
AGE2E-Core-Mikroscope
AGE2E-Core-Provisioning-Templates
AGE2E-Tooling-MetadataService
AGE2E-Core-DevOps-Dashboard
AGE2E-Core-Mikroscope-Web
AGE2E-Core-Provisioning-Workload
AGE2E-Tooling-ReportingService
AGE2E-Core-Infrastructure
AGE2E-Core-Mikroscope-test
AGE2E-Tooling-HistoricalReporting
AGE2E-Tooling-Tools
AGE2E-Core-Intrinsic
AGE2E-Core-NoOp-Example
AGE2E-Tooling-Infrastructure
AGE2E-Workload-EP-Validation
)

for repo in ${repository_list[*]}
do
 echo "Repository: $repo"
 cd $repo
 git fetch -p
 git for-each-ref --format='%(committerdate) %09 %(authorname) %09 %(refname)'  --sort=author refs/remotes | grep origin
 echo " "
 cd ..
done


### Run this script
# bash fetch_repo_branches.sh > list_repos_branches.txt

## Remove the HEAD and Master branch from output list
# sed -i '' '/HEAD/d' ./list_repos_branches.txt
# sed -i '' '/master/d' ./list_repos_branches.txt
