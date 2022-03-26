import github.Repository

import pyGithubClient
import requests

github_client = pyGithubClient.setup()

# for issue in github.Repository.Repository.get_issues():
#     print(issue)


# plotly_repo = github_client.get_repo('plotly/plotly')
#
# paginated_issues = plotly_repo.get_issues(state="all").get_page(1)
# '''
# Stage 1: First page of issues for Plotly
# '''
# for head_level_issue in paginated_issues:
#     full_issue = plotly_repo.get_issue(head_level_issue.number)
#     print(full_issue)
#
# print(f'Default length of page: {len(paginated_issues)}')


'''
Stage 2: All commits for Plotly
'''

# repo = github_client.get_repo("plotly/plotly")
#
# for repo in repo.get_issues(state="all", page=2, per_page=15):
#     print(repo)

owner = "plotly"
repoName = "plotly"
r = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues', headers={'Authorization' : pyGithubClient.pull_access_token()})
print(r)
if r.status_code == 200:
    print(r.text)
