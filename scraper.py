"""
This module contains a function to search Google Scholar using Selenium and BeautifulSoup.
It uses mobile emulation and can optionally use a proxy.
"""

#TODO: Implement a caching server
#TODO: Use a better method for the proxy list

import json
import requests
import time
import urllib.parse
import random
import argparse
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Handle the proxy stuff
proxies = []

def init_proxies():
    global proxies
    proxy_string = os.getenv('PROXIES', '')  # Default to an empty string if not set
    proxies = [p.strip() for p in proxy_string.split(',')] if proxy_string else []

def test_proxy(proxy):
    """
    Test if the proxy is working by attempting to access a website.
    Returns True if the proxy is working, False otherwise.
    """
    try:
        response = requests.get('http://www.google.com', proxies={"http": proxy, "https": proxy}, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to connect using proxy {proxy}: {e}")
        return False

def get_working_proxy():
    """
    Tries to find a working proxy from the list, testing each up to max_attempts times.
    Returns a working proxy or None if none are working after the attempts.
    """
    global proxies
    random.shuffle(proxies)
    #Try 5 proxies for 3 times each, if none work, return None
    attempts = 5
    while attempts > 0:
        proxy = proxies.pop()
        if test_proxy(proxy):
            print(f"Proxy {proxy} is working, using it for the search.")
            return proxy
        attempts -= 1
        print(f"Proxy {proxy} failed, Attempt: {5 - attempts}.")
    print("No working proxies found after maximum attempts.")
    return None

def search_scholar(search_key, proxy=None):
    """
    This function searches Google Scholar using Selenium and BeautifulSoup.
    It uses mobile emulation and can optionally use a proxy.
    """
    # Validate the search key
    if not search_key:
        raise ValueError("The search key is empty or invalid.")
    if not isinstance(search_key, str):
        raise ValueError("The search key must be a string.")
    
    # Set up the driver
    try:
        mobile_emulation = { "deviceName": "Nexus 5" }
        options = Options()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument("--headless") # Ensure GUI is off
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=webdriver_service)
    except Exception as e:
        raise Exception(f"Failed to initialize the WebDriver: {e}")
    # open first result in preview mode
    path = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={}&btnG='
    path = path.format(urllib.parse.quote_plus(search_key))
    driver.get(path)
    time.sleep(1)
    click_for_preview_elements = driver.find_elements(By.XPATH, '//h3[@class="gs_rt"]//a')
    cnt = 0
    pubs = []
    click_for_preview_elements[0].click()  # Click on the first preview element

    while cnt < len(click_for_preview_elements):
        try:
            # wait until the preview is loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="gs_qabs_panel"]')))
            pub_infos = driver.find_elements(By.XPATH, '//div[@class="gs_qabs_panel"]')

            for pub_info in pub_infos:
                try:
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
                    # Extract the publication year
                    year_element = soup.find(class_="gs_qabs_pub")
                    year = year_element.get_text(strip=True).split(",")[-1] if year_element else None

                    # Append the formatted data to the list
                    if title and abstract and article_link and authors and citations > 0:
                        pub_data = {
                            "title": title,
                            "abstract": abstract,
                            "article_link": article_link,
                            "authors": authors,
                            "citations": citations,
                            "year": year
                        }
                        pubs.append(pub_data)
                except Exception as e:
                    print(f"Error occurred while extracting publication information: {e}")

            # Go to the next preview
            next_button = driver.find_element(By.XPATH, '//a[@class="gs_psd_prt"]')
            next_button.click()
            time.sleep(0.4)
            cnt += 1
        except Exception as e:
            print(f"Error occurred while navigating to the next preview: {e}")

    return pubs

#Uncomment when running without API

# parser = argparse.ArgumentParser(description='Search Google Scholar')
# parser.add_argument('-k', '--keyword', type=str, help='Keyword to search for')
# args = parser.parse_args()

# # Before calling search_scholar, check for a working proxy
# init_proxies()
# working_proxy = get_working_proxy(proxies)
# if working_proxy:
#     res = search_scholar(args.keyword, working_proxy)
#     with open('res.json', 'w', encoding='utf-8') as f:
#         json.dump(list(res), f, indent=4)
# else:
#     print("Error: No working proxies available.")