import auth
import requests
import json
import csv
import sys

owner = "plotly"
repoName = "plotly"

'''
Stage 1: Issues for Plotly
'''
# look at this link for example: https://api.github.com/repositories/14579179/issues?page=1&per_page=100&state=all
with open("stage1_data.csv", 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar= '|', quoting=csv.QUOTE_MINIMAL)
    page = 1
    #set headers
    csv_writer.writerow(["Index of Issue", "State", "Labels", "Assignees", "Comments", "Closed At", "Created At", "Locked", "Page of Response"])

    #get ONE page
    response_stage1 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues?page=1&per_page=100&state=all', auth=(auth.populate_git_username(), auth.pull_access_token()))
    body = json.loads(response_stage1.content)
    print(f'stage 1 response code {response_stage1.status_code}')
    #get ALL the rest of the pages of issues until we reach the end
    while response_stage1.status_code == 200 and bool(body):


        # We don't need to concatenate the new JSON since we're outputting it to a csv, so let's just write directly to csv
        for index, issue in enumerate(body):
            csv_writer.writerow([index, issue["state"], issue["labels"], issue["assignees"], issue["comments"], issue["closed_at"], issue["created_at"], issue["locked"], page])

        #Increment page for the next 100 issues
        page += 1
        response_stage1 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues?page={page}&per_page=100&state=all', auth=(auth.populate_git_username(), auth.pull_access_token()))
        body = json.loads(response_stage1.content)

csvfile.close()

'''
Stage 2: A page of commits for Plotly
'''
with open("stage2_data.csv", 'w', newline='') as csvfile2:
    csv_writer2 = csv.writer(csvfile2, delimiter=',', quotechar= '|', quoting=csv.QUOTE_MINIMAL)
    page = 1
    commit_url_list_of_sha = []

    csv_writer2.writerow(["Index of Commit", "Committer Name", "Committer Date", "Tree URL", "Page of Response"])

    # Get first page
    response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page={page}&per_page=100',  auth=(auth.populate_git_username(), auth.pull_access_token()))
    # response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page={page}&per_page=100')
    body = json.loads(response_stage2.content)
    print(f'stage 2 response code {response_stage2.status_code}')

    #get ALL the rest of the pages pages
    while response_stage2.status_code == 200 and bool(body):

        for index, commit_response in enumerate(body):
            commit_json = commit_response["commit"]
            committer_json = commit_json["committer"]
            tree_json = commit_json["tree"]
            csv_writer2.writerow([index, committer_json["name"], committer_json["date"], tree_json["url"], page])
            commit_url_list_of_sha.append(tree_json["sha"])

        page += 1
        response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page={page}&per_page=100',  auth=(auth.populate_git_username(), auth.pull_access_token()))
        body = json.loads(response_stage2.content)

csvfile2.close()

'''
Stage 3: Code Size for Plotly
'''
with open("stage3_data.csv", 'w', newline='') as csvfile3:
    csv_writer3 = csv.writer(csvfile3, delimiter=',', quotechar= '|', quoting=csv.QUOTE_MINIMAL)
    page = 1
    # print(commit_url_list_of_sha)

    csv_writer3.writerow(["Index of Commit", "SubIndex of Commit", "Size", "Path"])
    for index, commit_url_sha in enumerate(commit_url_list_of_sha):
        response_stage3 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/git/trees/{commit_url_sha}', auth=(auth.populate_git_username(), auth.pull_access_token()))
        # response_stage3 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/git/trees/{commit_url_sha}')
        body = json.loads(response_stage3.content)
        tree_array_json = body["tree"]
        for sub_index, tree_node in enumerate(tree_array_json):
            print(tree_node)
            if 'size' in tree_node:
                csv_writer3.writerow([index, sub_index, tree_node["size"], tree_node["path"]])
csvfile3.close()
