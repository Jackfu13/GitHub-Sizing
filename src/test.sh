curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <token>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -o output.json
  https://api.github.com/user/repos