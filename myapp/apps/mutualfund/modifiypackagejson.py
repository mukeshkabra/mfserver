import json
with open("/Users/8398/Desktop/package.json","r") as f:
    json_data=json.load(f)
    
    json_data["devDependencies"]["rn-batbelt"]="mukesh"
with open("/Users/8398/Desktop/package.json","w+") as f:
    f.write(json.dumps(json_data))
