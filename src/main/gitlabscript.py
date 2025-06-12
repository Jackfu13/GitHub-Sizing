import requests
import os
import json
import certifi
requests.packages.urllib3.disable_warnings()
 # Retrieve token from environment variable
 #token = input("Enter your PAT token: ")
#url = input("Enter the API endpoint url: ")
#
#https://gitlab.com/api/v4/projects
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
        newUrl = f'https://gitlab.com/api/v4/projects/{repo["id"]}/members'
        response = requests.get(newUrl, headers=headers,verify=False)
        if response.status_code==200:
            members = response.json()
            memberList = []
            for member in members:
                newDict = {}
                newDict["id"] = member["id"]
                newDict["username"] = member["username"]
                memberList.append(newDict)
            dict["members"] = memberList
            dict["id"] = repo["id"]
            dict["project_name"] = repo["name"]
            dict["owner"] = repo["namespace"]["name"]
            dict["storage_size"] = repo["statistics"]["storage_size"]/1000
            dict["repository_size"] = repo["statistics"]["repository_size"]/1000
            statList.append(dict)
        else:
            quit()

        

    with open('gitlabdata.json', 'w') as file:
        json.dump(statList, file, indent=4)
        print("Filtered data saved to gitlabdata.json")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
  