from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Fetch necessary inputs from environment variables
github_token = os.getenv('GITHUB_TOKEN')  # Use GitHub secret for PAT
repo_name = os.getenv('REPO_NAME')
tag_pattern = os.getenv('TAG_PATTERN')
environment = os.getenv('ENVIRONMENT')

# GitHub login credentials (Use PAT as password)
github_username = 'saikiranrko'  # Replace with your GitHub username
github_password = "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"  # Assign the GitHub PAT to the password variable

# Configure WebDriver (using ChromeDriver)
options = Options()
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
WebDriverWait(driver, 30).until(EC.url_changes('https://github.com/login'))  # Increased wait time

# Navigate to the repository settings page
driver.get(f'https://github.com/{repo_name}/settings')

# Wait for the settings page to load (increased timeout)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-content="Environments"]')))

# Take a screenshot to debug
driver.save_screenshot('screenshot.png')  # This will save a screenshot to the current working directory

# Find the "Environments" link using CSS selector (more reliable in some cases)
driver.find_element(By.CSS_SELECTOR, 'span[data-content="Environments"]').click()

# Wait for the environments page to load
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.LINK_TEXT, environment)))

# Click on the environment to configure
driver.find_element(By.LINK_TEXT, environment).click()

# Wait for the environment settings page to load
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'tagPattern')))  # Adjust as necessary

# Add the tag protection pattern in the environment settings
tag_input = driver.find_element(By.NAME, 'tagPattern')  # Adjust the selector if necessary
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
