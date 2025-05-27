curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <Token>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -o src\\output.json \
  --url https://api.github.com/user/repos