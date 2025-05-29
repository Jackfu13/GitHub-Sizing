import requests
import os
import json
import certifi
 # Retrieve token from environment variable
token = input("Please enter your PAT token: ")
url = input("Enter the API endpoint url: ")
headers = {'Authorization': f'token {token}'}
response = requests.get(url, headers=headers)


if response.status_code == 200:
    
    repos = response.json()
    with open('output//data.json', 'w') as file:
        json.dump(repos, file, indent=4)
    print("json saved to output/data.json")
else:
        print(f"Error: {response.status_code}")
        print(response.text)