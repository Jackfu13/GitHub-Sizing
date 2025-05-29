import json
import subprocess
x = subprocess.run(['C:\Program Files\Git\\bin\\bash.exe','src//main//test.sh'])
# Open and load the JSON file
with open('output\\output.json', 'r') as file:
    data = json.load(file)

# Access the data
sizeList = []
for object in data:
    dict = {}
    dict["repoName"] = object["name"]
    size  = object["size"]/1000
    dict["size"] = size
    sizeList.append(dict)

with open('output//final.json', 'w') as file:
    json.dump(sizeList, file, indent=4)

