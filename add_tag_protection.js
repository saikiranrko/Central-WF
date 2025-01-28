const axios = require('axios');

// Fetch environment variables
const githubToken = process.env.GITHUB_TOKEN;  // Ensure this is correctly set in GitHub Actions Secrets
const repoName = process.env.REPO_NAME;
const tagPattern = process.env.TAG_PATTERN;
const environment = process.env.ENVIRONMENT;

// Check if the token is present
if (!githubToken) {
  console.error("Error: GITHUB_TOKEN is not set.");
  process.exit(1);
}

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
    process.exit(1);  // Exit with error code 1 if there's an issue
  }
}

// Run the function
addTagProtection();
