import pyGithubClient

github_client = pyGithubClient.setup()

repo = github_client.get_repo("plotly/plotly")

for repo in repo.get_issues():
    print(repo)
