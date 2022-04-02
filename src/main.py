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
    response_stage1 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues?page=1&per_page=100&state=all', auth=('nhb15', auth.pull_access_token()))
    body = json.loads(response_stage1.content)
    print(response_stage1.status_code)
    #get ALL the rest of the pages of issues until we reach the end
    while response_stage1.status_code == 200 and bool(body):


        # We don't need to concatenate the new JSON since we're outputting it to a csv, so let's just write directly to csv
        for index, issue in enumerate(body):
            csv_writer.writerow([index, issue["state"], issue["labels"], issue["assignees"], issue["comments"], issue["closed_at"], issue["created_at"], issue["locked"], page])

        #Increment page for the next 100 issues
        page += 1
        response_stage1 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/issues?page={page}&per_page=100&state=all', auth=('nhb15', auth.pull_access_token()))
        body = json.loads(response_stage1.content)

csvfile.close()

'''
Stage 2: A page of commits for Plotly
'''
with open("stage2_data.csv", 'w', newline='') as csvfile2:
    csv_writer2 = csv.writer(csvfile2, delimiter=',', quotechar= '|', quoting=csv.QUOTE_MINIMAL)
    page = 1
    csv_writer2.writerow(["Index of Commit", "Committer Name", "Committer Date", "Tree URL", "Page of Response"])

    # Get first page
    # response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page={page}&per_page=100',  auth=('nhb15', auth.pull_access_token()))
    response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page={page}&per_page=100')
    body = json.loads(response_stage2.content)

    #get ALL the rest of the pages pages
    while response_stage2.status_code == 200 and bool(body):
        body = json.loads(response_stage2.content)
        print(f'stage 2 response code {response_stage2.status_code}')

        for index, commit_response in enumerate(body):
            print(commit_response)
            print(commit_response["commit"])
            commit_json = commit_response["commit"]
            committer_json = commit_json["committer"]
            tree_json = commit_json["tree"]
            csv_writer2.writerow([index, committer_json["name"], committer_json["date"], tree_json["url"], page])

        page += 1
        response_stage2 = requests.get(f'https://api.github.com/repos/{owner}/{repoName}/commits?page={page}&per_page=100')
        body = json.loads(response_stage2.content)

csvfile2.close()

sys.exit()

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

sys.exit()
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
        print(f'stage 3 still in progress - body: {body}')

        # for index, git_tree in enumerate(body):
            # print(index)
            # print(git_tree)