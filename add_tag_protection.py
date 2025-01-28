from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Fetch necessary inputs from environment variables
github_token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('REPO_NAME')
tag_pattern = os.getenv('TAG_PATTERN')
environment = os.getenv('ENVIRONMENT')

# GitHub login credentials (Use PAT as password)
github_username = 'saikiranrko'  # Replace with your username or use secrets
github_password = sai@96037

# Configure WebDriver (using ChromeDriver)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to GitHub login page
driver.get('https://github.com/login')

# Log in to GitHub
driver.find_element(By.ID, 'login_field').send_keys(github_username)
driver.find_element(By.ID, 'password').send_keys(github_password)
driver.find_element(By.NAME, 'commit').click()

# Wait for the login to complete
time.sleep(5)

# Navigate to the repository settings page
driver.get(f'https://github.com/{repo_name}/settings')

# Wait for the settings page to load
time.sleep(5)

# Navigate to the "Environment" settings section
driver.find_element(By.PARTIAL_LINK_TEXT, 'Environments').click()

# Wait for the environments page to load
time.sleep(3)

# Click on the environment to configure
driver.find_element(By.LINK_TEXT, environment).click()

# Wait for the environment settings page to load
time.sleep(3)

# Add the tag protection pattern in the environment settings
tag_input = driver.find_element(By.NAME, 'tagPattern')  # This is hypothetical
tag_input.clear()
tag_input.send_keys(tag_pattern)

# Save the tag protection pattern
driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]").click()

# Wait for the action to complete
time.sleep(2)

# Print success message
print("Tag protection pattern set successfully!")

# Close the browser
driver.quit()
