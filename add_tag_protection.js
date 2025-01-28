const axios = require('axios');

// Fetch environment variables
const githubToken = process.env.GITHUB_TOKEN;
const repoName = process.env.REPO_NAME;
const tagPattern = process.env.TAG_PATTERN;
const environment = process.env.ENVIRONMENT;

const apiUrl = `https://api.github.com/repos/${repoName}/environments/${environment}`;

async function addTagProtection() {
  try {
    // Headers for authentication
    const headers = {
      'Authorization': `Bearer ${githubToken}`,
      'Accept': 'application/vnd.github+json',
    };

    // Define the payload for the environment protection
    const payload = {
      "deployment_branch_policy": {
        "protected_branches": false,
        "custom_branch_policies": true
      },
      "tag_pattern": tagPattern // This would ideally be added if supported
    };

    // Make API request to create/update environment protection
    const response = await axios.put(apiUrl, payload, { headers });

    console.log("Environment protection added successfully!");
    console.log(response.data);
  } catch (error) {
    console.error("Error adding tag protection:", error.response ? error.response.data : error.message);
  }
}

// Run the function
addTagProtection();
