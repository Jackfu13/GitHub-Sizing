import json

# Open and load the JSON file
with open('output2.json', 'r') as file:
    data = json.load(file)

# Access the data
sizeList = []
for object in data:
    dict = {}
    dict["repoName"] = object["name"]
    size  = object["size"]/1000
    dict["size"] = size
    sizeList.append(dict)

with open('final.json', 'w') as file:
    json.dump(sizeList, file, indent=4)

