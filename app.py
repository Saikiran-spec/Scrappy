import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import spacy

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Setup WebDriver using webdriver_manager to automatically handle the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# LinkedIn Login Credentials (Never hardcode sensitive data in production)
username = ""
password = ""

# Function to login to LinkedIn
def login():
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    # Input username and password
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)  # Wait for login to complete

# Function to scrape profile data
def scrape_profile():
    driver.get("https://www.linkedin.com/in/your-profile/")  # Replace with target profile URL
    time.sleep(3)

    # Use BeautifulSoup to parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract profile name
    profile_name = soup.find('h1', {'class': 'text-heading-xlarge'}).text.strip()
    print(f"Profile Name: {profile_name}")

    # Scrape additional profile info (example: job title, location)
    job_title = soup.find('div', {'class': 'text-body-medium'}).text.strip() if soup.find('div', {'class': 'text-body-medium'}) else "Not available"
    print(f"Job Title: {job_title}")

# Function to scrape messages
def scrape_messages():
    driver.get("https://www.linkedin.com/messaging/")  # LinkedIn messaging page
    time.sleep(3)

    # Extract message data
    messages = driver.find_elements(By.CSS_SELECTOR, ".msg-s-message-list")
    for message in messages:
        print(f"Message: {message.text}")

# Function for NLP processing using spaCy
def process_text(text):
    doc = nlp(text)
    for ent in doc.ents:
        print(f"{ent.text} - {ent.label_}")  # Print named entities (e.g., people, organizations)

# Main Execution
if __name__ == "__main__":
    login()
    scrape_profile()
    scrape_messages()

    # Example: Use NLP processing on a scraped message
    sample_message = "John Doe is working as a Software Engineer at XYZ Corp."
    print("\nNLP Processing Output:")
    process_text(sample_message)

    # Close the browser
    driver.quit()
