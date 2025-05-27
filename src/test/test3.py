import requests
import os
import json
 # Retrieve token from environment variable
token = os.environ.get("")
    
headers = {'Authorization': f'token <token>'}
response = requests.get('https://api.github.com/user/repos', headers=headers)

filter = []
if response.status_code == 200:
    
    repos = response.json()

    for repo in repos:
    
        response2 = requests.get(f"https://api.github.com/repos/{repo["owner"]["login"]}/{repo["name"]}/collaborators",headers = headers)
        clist = []
        if response.status_code==200:
            collaborators = response2.json()
            for user in collaborators:
                 clist.append(user["login"])
        else:
            print(f"Error: {response2.status_code}")
            print(response2.text)
            
        reps = {}
        reps["name"] = repo["name"]
        reps["owner"] = repo["owner"]["login"]
        reps["size"] = repo["size"]
        reps["collaborators"] = clist
        filter.append(reps)
    with open('src//data.json', 'w') as file:
        json.dump(filter, file, indent=4)
    
else:
        print(f"Error: {response.status_code}")
        print(response.text)