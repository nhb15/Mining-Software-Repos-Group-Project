from github import Github
import os
from dotenv import load_dotenv

def setup():
    authenticated_github_instance = Github(pull_access_token())

    # print(f'Your github token in .env reads: {os.environ.get("GITHUB_ACCESS_TOKEN")}')
    return authenticated_github_instance

def pull_access_token():
    load_dotenv()

    return os.environ.get('GITHUB_ACCESS_TOKEN')



