import requests
import json

def download_issues_from_Github(token):
    url = "https://api.github.com/repos/angular/angular/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "state": "all",
        "per_page": 100
    }
    
    issues = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            issues += response.json()
            # Update the url variable with the link to the next page of results
            url = response.links.get('next', {}).get('url')
        else:
            print(f"Failed to retrieve issues. Status code: {response.status_code}")
            break
    
    with open("angular_issues.json", "w") as f:
        json.dump(issues, f)

token = "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"
download_issues_from_Github(token)
