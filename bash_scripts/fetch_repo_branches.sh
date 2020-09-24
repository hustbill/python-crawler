#!/bin/bash
## filename: fetch_repo_branches.sh

repository_list=(
PP-Core-Base
PP-Core-Mikroscope
PP-Core-Provisioning-Templates
PP-Tooling-MetadataService
PP-Core-DevOps-Dashboard
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
