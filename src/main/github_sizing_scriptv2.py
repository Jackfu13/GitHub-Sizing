import requests
import os
import json
import certifi
 # Retrieve token from environment variable
token = input("Enter your PAT token: ")
url = input("Enter the API endpoint url: ")
headers = {'Authorization': f'token {token}'}
response = requests.get(url, headers=headers)


if response.status_code == 200:
    
    repos = response.json()
    with open('rawdata.json', 'w') as file:
        json.dump(repos, file, indent=4)
    filter = []
    for repo in repos:
        reps = {}
        reps["name"] = repo["name"]
        reps["owner"] = repo["owner"]["login"]
        reps["size"] = repo["size"]
        filter.append(reps)
    with open('filterdata.json', 'w') as file:
        json.dump(filter, file, indent=4)
    print("json saved to data.json")
else:
        print(f"Error: {response.status_code}")
        print(response.text)