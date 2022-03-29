import auth
import requests
import json

owner = "plotly"
repoName = "plotly"

'''
Stage 1: First page of issues for Plotly
'''
response_stage1 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues?page=1&per_page=100&state=all', auth=('nhb15', auth.pull_access_token()))
print(response_stage1)
if response_stage1.status_code == 200:
    body = json.loads(response_stage1.content)

    for index, issue in enumerate(body):
        print(index)
        # print(issue['number'])

'''
Stage 2: A page of commits for Plotly
'''
response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page=1&per_page=100',  auth=('nhb15', auth.pull_access_token()))

commit_url_list = []
if response_stage2.status_code == 200:
    body = json.loads(response_stage2.content)

    for index, commit in enumerate(body):
        print(index)
        commit_url_list.append(commit['url'])
print(commit_url_list)
'''
Stage 3: Code Size for Plotly
'''
# sample commit
for commit_url in commit_url_list[0:2]:
    response_stage3 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/git/trees/{commit_url}?recursive=true',  auth=('nhb15', auth.pull_access_token()))
    print(response_stage3)
    if response_stage3.status_code == 200:
        body = json.loads(response_stage3.content)

        for index, git_tree in enumerate(body):
            print(index)
            print(git_tree)