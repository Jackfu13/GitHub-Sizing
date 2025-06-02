import json
import subprocess
x = subprocess.run(['C:\Program Files\Git\\bin\\bash.exe','src//main//size.sh'])


with open('output.json', 'r') as file:
    data = json.load(file)

# Access the data
sizeList = []
for object in data:
    dict = {}
    dict["repoName"] = object["name"]
    dict["owner"] = object["owner"]["login"]
    size  = object["size"]/1000
    dict["size"] = size
    sizeList.append(dict)

with open('final.json', 'w') as file:
    json.dump(sizeList, file, indent=4)
