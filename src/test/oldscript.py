import json

with open('output.json', 'r') as file:
    data = json.load(file)

# Now you can work with the 'data' variable
for dat in data:
    print(dat["name"])

with open('test.json', 'w') as file:
        json.dump(data, file, indent=4)
  