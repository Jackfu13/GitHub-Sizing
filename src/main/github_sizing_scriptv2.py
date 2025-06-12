import requests
import os
import json
import certifi
requests.packages.urllib3.disable_warnings()
 # Retrieve token from environment variable
token = input("Enter your PAT token: ")
url = input("Enter the API endpoint url: ")
headers = {'Authorization': f'token {token}'}
response = requests.get(url, headers=headers,verify=False)


if response.status_code == 200:
    
    repos = response.json()
    with open('rawgithubdata.json', 'w') as file:
        json.dump(repos, file, indent=4)
    print("Saved to rawgithubdata.json")
    filter = []
    for repo in repos:
        url = f'https://api.github.com/repos/{repo["owner"]["login"]}/{repo["name"]}/collaborators'
        response = requests.get(url,verify=False,headers = headers)
        
        if response.status_code==200:
            collab = response.json()
            cl = []
            for collaborators in collab:
                 dicts = {}
                 dicts["username"] = collaborators["login"]
                 dicts["id"] = collaborators["id"]
                 cl.append(dicts)
            reps = {}
            reps["repo_name"] = repo["name"]
            reps["collaborators"] = cl
            reps["owner"] = repo["owner"]["login"]
            reps["size"] = repo["size"]
            filter.append(reps)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    with open('githubdata.json', 'w') as file:
        json.dump(filter, file, indent=4)
    print("saved to githubdata.json")
else:
        print(f"Error: {response.status_code}")
        print(response.text)