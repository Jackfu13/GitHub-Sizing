import requests
import os
import json
import certifi
 # Retrieve token from environment variable
 #token = input("Enter your PAT token: ")
#url = input("Enter the API endpoint url: ")
token = "glpat-nQgadghwKVL7KhpCNv17"
headers = {'PRIVATE-TOKEN': f'{token}'}
params = {"membership": True, "per_page": 100,"statistics":True}
response = requests.get(url = "https://gitlab.com/api/v4/projects", headers=headers,verify=False,params = params)


if response.status_code == 200:
    data = response.json()
    with open('test.json', 'w') as file:
        json.dump(data, file, indent=4)
  