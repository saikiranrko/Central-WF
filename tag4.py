import os
import requests

owner = 'saikiranrko'
# Replace with your GitHub Token, Org Name, Repo Name, and Environment Name
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("ORG_NAME")
REPO_NAME = os.getenv("REPO_NAME")
ENV_NAME = os.getenv("ENV_NAME")

# GitHub GraphQL API URL
GRAPHQL_URL = "https://api.github.com/graphql"

# GraphQL Query to fetch branch protection rules
query = f"""
{{
  repository(owner: "{ORG_NAME}", name: "{REPO_NAME}") {{
    branchProtectionRules(first: 100) {{
      edges {{
        node {{
          pattern
        }}
      }}
    }}
  }}
}}
"""

# Headers for authentication
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

# Function to update deployment branch policy
def update_deployment_branch_policy():
    url = f"https://api.github.com/repos/{owner}/{repo}/environments/{environment}"
    payload = {
        "deployment_branch_policy": {
            "protected_branches": False,
            "custom_branch_policies": True,
            "custom_branches": [
                "v*",
                "release-*"
            ]
        }
    }
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Deployment branch policy updated successfully")
    else:
        print(f"Error updating deployment branch policy: {response.status_code}, {response.text}")

# Update deployment branch policy
update_deployment_branch_policy()

# Make the request to fetch existing branch protection rules
response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers, timeout=10)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    # Extracting branch protection patterns
    branch_patterns = [rule["node"]["pattern"] for rule in data["data"]["repository"]["branchProtectionRules"]["edges"]]
    print("Protected Branch Patterns:")
    for pattern in branch_patterns:
        print(f"- {pattern}")
else:
    print(f"Error: {response.status_code}, {response.text}")
    branch_patterns = []

# Function to create branch protection rule
def create_protection_rule(pattern, reftype):
    url = f"https://api.github.com/repos/{ORG_NAME}/{REPO_NAME}/environments/{ENV_NAME}/deployment-branch-policies"
    payload = {
        "name": pattern
    }
    if reftype == "tag":
        payload["type"] = "tag"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"Protection rule created for {reftype}: {pattern}")
    elif response.status_code == 406:
        print(f"Protection rule for {reftype}: {pattern} already exists")
    else:
        print(f"Error creating protection rule for {reftype}: {pattern}, {response.status_code}, {response.text}")

# Create protection rules for both reftype:tag and reftype:branch
for pattern in branch_patterns:
    create_protection_rule(pattern, "branch")
    create_protection_rule(pattern, "tag")
