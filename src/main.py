import auth
import requests
import json

owner = "plotly"
repoName = "plotly"

'''
Stage 1: First page of issues for Plotly
'''
response_stage1 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues?page=1&per_page=100&state=all', auth=('nhb15', auth.pull_access_token()))
print(f'stage 1 status code: {response_stage1}')
if response_stage1.status_code == 200:
    body = json.loads(response_stage1.content)

    # look at this link for example: https://api.github.com/repositories/14579179/issues?page=1&per_page=100&state=all
    for index, issue in enumerate(body):
        print(f'index of issue in our page: {index}')
        print(f'state: {issue["state"]}')
        print(f'labels: {issue["labels"]}')
        print(f'assignees: {issue["assignees"]}')
        print(f'comments: {issue["comments"]}')
        print(f'closed_at: {issue["closed_at"]}')
        print(f'created_at: {issue["created_at"]}')
        print(f'locked: {issue["locked"]}')

    # print(issue['number'])

'''
Stage 2: A page of commits for Plotly
'''
response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page=1&per_page=100',  auth=('nhb15', auth.pull_access_token()))
print(f'stage 2 status code: {response_stage2}')

commit_url_list = []
if response_stage2.status_code == 200:
    body = json.loads(response_stage2.content)

    # look at this example link for body formatting https://api.github.com/repositories/14579179/commits?page=1&per_page=100
    for index, commit in enumerate(body):
        commit_url_list.append(commit['url'])
        # FIXME: Need to add attributes requested here
print(f'START COMMIT URL LIST')
print(commit_url_list)
print(f'END COMMIT URL LIST')
'''
Stage 3: Code Size for Plotly
'''
# sample commit
for commit_url in commit_url_list:
    commit_deep_dive = requests.get(f'{commit_url}', auth=('nhb15', auth.pull_access_token()))
    body = json.loads(commit_deep_dive.content)
    # if you click on one of the links populated from stage 2, you can see the output of the get request in line 39
    # we have the "sha" attribute at the top as well as a "tree" attribute that has a "sha" beneath it. My guess is that's where recursion comes in

    response_stage3 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/git/trees/{body["sha"]}?recursive=true', auth=('nhb15', auth.pull_access_token()))
    if response_stage3.status_code == 200:
        body = json.loads(response_stage3.content)
        print('stage 3 still in progress')

        # for index, git_tree in enumerate(body):
            # print(index)
            # print(git_tree)