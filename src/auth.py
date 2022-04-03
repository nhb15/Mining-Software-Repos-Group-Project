import os
from dotenv import load_dotenv

def pull_access_token():
    load_dotenv()

    return os.environ.get('GITHUB_ACCESS_TOKEN')

def populate_git_username():
    load_dotenv()

    return os.environ.get('GITHUB_USER_NAME')


