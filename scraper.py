"""
This module contains a function to search Google Scholar using Selenium and BeautifulSoup.
It uses mobile emulation and can optionally use a proxy.
"""

#TODO: Error handeling for the inner for loop and the while loop
#TODO: Error handeling for the proxy list for a quick fix
#TODO: Error handeling for the search key
#TODO: Error handeling for the webdriver
#TODO: Use a better method for the proxy list

import json
import time
import urllib.parse
import random
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


def search_scholar(search_key, proxy=None):
    """
    This function searches Google Scholar using Selenium and BeautifulSoup.
    It uses mobile emulation and can optionally use a proxy.
    """
    # Set up the driver
    mobile_emulation = { "deviceName": "Nexus 5" }

    options = Options()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument("--headless") # Ensure GUI is off
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=webdriver_service)
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    # open first result in priview mode
    path = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}&btnG='
    path = path.format(urllib.parse.quote_plus(search_key))
    driver.get(path)
    time.sleep(1)
    click_for_preview_elements = driver.find_elements(By.XPATH, '//h3[@class="gs_rt"]//a')
    cnt = 0
    pubs = set()
    click_for_preview_elements[0].click()  # Click on the first preview element

    while cnt < len(click_for_preview_elements):
        print(cnt)
        # wait until the preview is loaded
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gs_qabs_panel"]')))
        pub_infos = driver.find_elements(By.XPATH, '//div[@class="gs_qabs_panel"]')

        for pub_info in pub_infos:

            soup = BeautifulSoup(pub_info.get_attribute('innerHTML'), 'html.parser')

            # Extract the title
            title_element = soup.find(class_="gs_qabs_title")
            title = title_element.get_text(strip=True) if title_element else None

            # Extract the abstract
            abstract_element = soup.find(class_="gs_qabs_snippet")
            abstract = abstract_element.get_text(strip=True) if abstract_element else None

            # Extract the links
            links = [a['href'] for a in soup.find_all('a', href=True)]
            article_link = links[1] if links else None

            # Extract the author names
            authors = []
            author_element = soup.find(class_="gs_qabs_au2")
            authors = author_element.get_text(strip=True) if author_element else None

            # Extract the number of citations
            citations_element = soup.find(class_="gs_qabs_gsl")
            citations = 0
            if citations_element:
                for li in citations_element.find_all('li'):
                    if li.text.startswith("Cited by"):
                        citations = int(li.text.split(" ")[2])
                        break

            # Append the formatted data to the list
            if title and abstract and article_link and authors and citations > 0:
                pubs.add((title, abstract, article_link, authors, citations))

        # Go to the next preview
        next_button = driver.find_element(By.XPATH, '//a[@class="gs_psd_prt"]')
        next_button.click()
        time.sleep(0.4)
        cnt += 1

    return pubs


# Handle the proxy stuff
# Format: IP:PORT \n IP:PORT \n ...
proxies = []
with open('proxy.txt', 'r', encoding="utf-8") as f:
    proxies = f.readlines()
proxies = [x.strip() for x in proxies]

parser = argparse.ArgumentParser(description='Search Google Scholar')
parser.add_argument('-k', '--keyword', type=str, help='Keyword to search for')
args = parser.parse_args()

# Then use args.keyword instead of 'deep learning'
res = search_scholar(args.keyword, random.choice(proxies))
with open('res.json', 'w', encoding='utf-8') as f:
    json.dump(list(res), f, indent=4)
