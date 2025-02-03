import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

def chrome(headless=False):
    # Create a Chrome service object with the updated path
    service = Service(executable_path=r"C:\Users\chittyreddy saikiran\Downloads\chromedriver_win32\chromedriver.exe")  # Corrected path here
    
    # Set Chrome options
    options = Options()
    if headless:
        options.add_argument("--headless")
    
    # Initialize the Chrome browser with service and options
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    return driver

# Pass False if you want to debug in visible mode
browser = chrome(False)

# Open LinkedIn login page
browser.get('https://www.linkedin.com/uas/login')
browser.implicitly_wait(3)

# Read login credentials from a file
file = open('config.txt')
lines = file.readlines()
username = lines[0].strip()  # Remove any extra spaces or newline characters
password = lines[1].strip()

# Find and fill in the login form
elementID = browser.find_element('id', 'username')
elementID.send_keys(username)

elementID = browser.find_element('id', 'password')
elementID.send_keys(password)

# Submit the login form
elementID.submit()

info = []

# List of LinkedIn profile links to scrape
links = ['https://www.linkedin.com/in/saikiran-chittyreddy-3a8846231/']

for link in links:
    browser.get(link)
    browser.implicitly_wait(1)

    def scroll_down_page(speed=8):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = browser.execute_script("return document.body.scrollHeight")

    scroll_down_page(speed=8)

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    # Get Name of the person
    try:
        name_div = soup.find('div', {'class': 'pv-text-details__left-panel mr5'})
        first_last_name = name_div.find('h1').get_text().strip()
    except:
        first_last_name = None
    
    # Get Talks about section info
    try:
        talksAbout_tag = name_div.find('div', {'class': 'text-body-small t-black--light break-words pt1'})
        talksAbout = talksAbout_tag.find('span').get_text().strip()
    except:
        talksAbout = None
    
    # Get Location of the Person
    try:
        location_tag = name_div.find('div', {'class': 'pb2'})
        location = location_tag.find('span').get_text().strip()
    except:
        location = None
    
    # Get Title of the Person
    try:
        title = name_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
    except:
        title = None
    
    # Get Company Link of the Person
    try:
        exp_section = soup.find('section', {'id': 'experience-section'})
        exp_section = exp_section.find('ul')
        li_tags = exp_section.find('div')
        a_tags = li_tags.find('a')
        company_link = a_tags['href']
        company_link = 'https://www.linkedin.com/' + company_link
    except:
        company_link = None

    # Get Job Title of the Person
    try:
        job_title = li_tags.find('h3', {'class': 't-16 t-black t-bold'}).get_text().strip()
    except:
        job_title = None
    
    # Get Company Name of the Person
    try:
        company_name = li_tags.find('p', {'class': 'pv-entity__secondary-title t-14 t-black t-normal'}).get_text().strip()
    except:
        company_name = None

    # Navigate to contact info page
    contact_page = link + 'detail/contact-info/'
    browser.get(contact_page)
    browser.implicitly_wait(1)

    contact_card = browser.page_source
    contact_page = BeautifulSoup(contact_card, 'lxml')
    
    # Get LinkedIn Profile Link and Contact details of the Person
    try:
        contact_details = contact_page.find('section', {'class': 'pv-profile-section pv-contact-info artdeco-container-card ember-view'})
        contacts = []
        for a in contact_details.find_all('a', href=True):
            contacts.append(a['href'])
    except:
        contacts = ['']

    info.append([first_last_name, title, company_link, job_title, company_name, talksAbout, location, contacts])
    time.sleep(5)

# Define the column names for the CSV file
column_names = ["Full Name", "Title", "Company URL", 'Job Title', 
                'Company Name', 'Talks About', 'Location', 'Profile Link and Contact']

# Create a DataFrame and save the data to a CSV file
df = pd.DataFrame(info, columns=column_names)
df.to_csv('data.csv', index=False)

print(".................Done Scraping!.................")
browser.quit()
