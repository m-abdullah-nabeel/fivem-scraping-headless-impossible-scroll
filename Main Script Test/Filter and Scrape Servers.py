#!/usr/bin/env python
# coding: utf-8

# ### Importing and setting up

# In[1]:


import time
from threading import Thread
import logging
import os
from datetime import datetime
import re

# import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains


# In[2]:


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'


# In[3]:


all_links = set()


# In[4]:


chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-session-crashed-bubble")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--suppress-message-center-popups")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("disable-infobars")

# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920x1080")

# chrome_options.add_argument("--no-first-run")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
# chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "test-type"])


# ### Essential Function in filtering

# In[5]:


def clearing_click_on_server():
    servers_clear_box_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/div[1]/div/a[1]'
    servers_clear_box = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, servers_clear_box_xpath))
    )
    servers_clear_box.click()


# In[6]:


def open_filter_dropdown():
    filter_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/section[2]/div/div[1]'
    filters = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, filter_xpath))
    )
    filters.click()
    time.sleep(10)


# ### 3 Core filtering functions

# In[7]:


def custom_server_search(server_name_to_search):
    search_bar_xpath = '//*[@id="searchBox"]'
    search_bar = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, search_bar_xpath))
    )
    search_bar.click()
    search_bar.send_keys(f'{server_name_to_search}', Keys.RETURN)
    
    clearing_click_on_server()    
    


# In[8]:


def filter_languages(language_name):
    open_filter_dropdown()
    languages_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/section[2]/div/div[3]/app-server-tag-filter/div/div[1]'
    language_filters = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, languages_xpath))
    )
    language_containing_xpath = f".//*[contains(text(), '{language_name}')]"
    language_clicks = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, language_containing_xpath))
    )
    time.sleep(4)
    language_clicks.click()
    clearing_click_on_server()    


# In[9]:


def filter_tags(tag_name):
    open_filter_dropdown()
    tags_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/section[2]/div/div[3]/app-server-tag-filter/div/div[2]/ul'    
    tag_filters = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, tags_xpath))
    )
    tag_click_action = ActionChains(driver)
    tag_click_action.move_to_element(tag_filters).scroll_by_amount(0, 500).perform()
    time.sleep(4)
    tag_containing_xpath = f".//*[contains(text(), '{tag_name}')]"
    print(tag_containing_xpath)
    tag_clicks = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, tag_containing_xpath))
    )
    tag_click_action = ActionChains(driver)
    tag_click_action.move_to_element(tag_clicks).click().perform()
    tag_clicks.click()
    clearing_click_on_server() 


# ### Main Script for scraping servers

# In[10]:


def scrape_server_links():
    print("Please write an estimate number of servers to scrape.")
    estimated_servers = int(input("A number only will work: "))
#     mind to keep on same page on all filtering
#     driver = webdriver.Chrome(service=Service(r"chromedriver.exe"), options=chrome_options)
#     driver.get('https://servers.fivem.net/servers')

    container_list_xpath = "//servers-list[1]//div[contains(@class, 'cdk-virtual-scroll-content-wrapper')]"

    container_list = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, container_list_xpath))
    )

    i = 0
    # for i in range(100):
    while len(all_links) < estimated_servers:
        i = i+1
        servers_loaded = WebDriverWait(container_list, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, './/servers-list-item//img'))
        )
        servers_loaded_no = len(servers_loaded) - 1
        print(f"Iteration {i}: Scraped a total of {servers_loaded_no} loaded servers.")
    #     print("The last loaded server text is: ", servers_loaded[servers_loaded_no].text)

        iteration_links = []

        for (i, images_loaded_server) in enumerate(servers_loaded):
            link_pict = images_loaded_server.get_attribute('src')
            server_id = link_pict.split('/')[-2]
    #         print(server_id)
            iteration_links.append(server_id)
    #         print(iteration_links)

        iteration_links = set(iteration_links)
        print(iteration_links)

        with open('Backup Links.txt', 'w') as f:
            for link in iteration_links:
                f.write(link)
                f.write('\n')

        print("These links are obtained in this iteration: ")
    #     print(iteration_links)
        print(len(iteration_links))
        all_links.update(iteration_links)
        print(len(all_links))

        time.sleep(5)
        last_loaded_server = ActionChains(driver)
        last_loaded_server.scroll_to_element(servers_loaded[servers_loaded_no]).perform()
        print("Scrolled to last server.")

    with open('All Links.txt', 'w') as f:
        for link in all_links:
            f.write(link)
            f.write('\n')

    print("Concluded with scraping!!!")
    print(f"Total {len(all_links)} servers scraped")


# In[11]:


# driver = webdriver.Chrome(service=Service(r"chromedriver.exe"), options=chrome_options)
# driver.get('https://servers.fivem.net/servers')
# scrape_server_links(driver)


# In[ ]:





# In[12]:


driver = webdriver.Chrome(service=Service(r"chromedriver.exe"), options=chrome_options)
driver.get('https://servers.fivem.net/servers')


# In[13]:


def setup_server_listings():
    print("Starting with scraping the results...")
    print("Please interact with following inputs to filter your servers.\n")
    
    print("Do you want to search by any custom server names?")
    print("""
    Note: you can search only one server name at this time,
    if you want to search multiple server names, you have to run this script multiple times.
    """)
    
    try:
        custom_bol = input("If yes, type 'y', otherwise skip custom server name search by entering no. ")
        if custom_bol == 'y':
            print("Write custom server name below.")
            custom_bol = input("Name: ")
            print("Going to search for: ")
            print(custom_bol.strip())
            custom_server_search(custom_bol.strip())        
    except Exception as Ex:
        print("There is an error in filtering by custom server name.")

    
    print("Do you want to filter by any language?")
    lang_bol = input("If yes, type 'y', otherwise skip language filtering by entering no. ")
    if lang_bol == 'y':
        print("Write comma separated names of languages below: ")
        lang_list = input("Languages: ")
        langs = lang_list.split(',')
        langs = [s.strip() for s in langs]
        
        print("Going to filter by: ")
        print(langs)
        for i in langs:
            try:                
                print(i)
                filter_languages(i)  
            except Exception as Ex:
                print(f"There is an error in filtering by language {i}. ")
                print(Ex)
    
    print("Do you want to filter by any tags?")
    tag_bol = input("If yes, type 'y', otherwise skip tags filtering by entering no. ")
    if tag_bol == 'y':
        print("Write comma separated tags below: ")
        tag_bol = input("Tags: ")
        tags = tag_bol.split(',')
        
        tags = [t.strip() for t in tags]
        print("Going to filter by: ")
        print(tags)
        
        for i in tags:
            try:                
                print(i)
                filter_tags(i)  
            except Exception as Ex:
                print(f"There is an error in filtering by tag {i}")
                print(Ex)
    
    try:
#         clearing_click_on_server()
        scrape_server_links() 
    except Exception as Ex:
        print("An error occured scraping a list of servers.")
        print(Ex)

    print("The script ended running successfully.")
    print("Thank you for working with me!")
    print("")


# In[ ]:





# In[14]:


setup_server_listings()


# In[15]:


# driver.quit()

