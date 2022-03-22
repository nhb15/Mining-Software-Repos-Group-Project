from github import Github
import os
from dotenv import load_dotenv

def setup():
    load_dotenv()

    authenticated_github_instance = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))

    # print(f'Your github token in .env reads: {os.environ.get("GITHUB_ACCESS_TOKEN")}')
    return authenticated_github_instance



