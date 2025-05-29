from pathlib import Path

employee_data = 'curl -L \\ \n  -H "Accept: application/vnd.github+json" \\ \n  -H "Authorization: Bearer <token>" \\ \n    -H "X-GitHub-Api-Version: 2022-11-28" \\ \n    -o output\\output.json \\ \n    --url https://api.github.com/user/repos'
file_path = Path("src\\test\\collab.sh")






file_path.write_text(employee_data)

'''
import subprocess
x = subprocess.run(['C:\\Program Files\\Git\\bin\\bash.exe','src//test//collab.sh'])
'''
