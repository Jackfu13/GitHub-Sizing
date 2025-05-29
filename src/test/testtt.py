from pathlib import Path

employee_data = 'curl -L \\ \n-H "Accept: application/vnd.github+json" \\ \n-H "Authorization: Bearer <token>" \\ \n-o output\\output.json \\ \n--url https://api.github.com/user/repos'
file_path = Path("src\\test\\collab.sh")

file_path.write_text(employee_data)

