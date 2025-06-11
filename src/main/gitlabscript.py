import requests
import os
import json
import certifi
 # Retrieve token from environment variable
 #token = input("Enter your PAT token: ")
#url = input("Enter the API endpoint url: ")
#token = "glpat-Z6H1KV7CNvW_rakP5q3c"
token = input("Please enter your Personal Access Token: ")
url = input("Please enter the API endpoint: ")
headers = {'PRIVATE-TOKEN': f'{token}'}
params = {"membership": True, "per_page": 100,"statistics":True}
response = requests.get(url, headers=headers,verify=False,params = params)


if response.status_code == 200:
    data = response.json()
    with open('rawgitlabdata.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Raw data saved to gitlabdata.json")
    statList = []
    for repo in data:
        dict = {}
        dict["id"] = repo["id"]
        dict["projectName"] = repo["name"]
        dict["owner"] = repo["namespace"]["name"]
        dict["statistics"] = repo["statistics"]
        statList.append(dict)

    with open('gitlabdata.json', 'w') as file:
        json.dump(statList, file, indent=4)
        print("Filtered data saved to gitlabdata.json")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
  