#!/usr/bin/env python
# coding: utf-8

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

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--window-size=1920x1080")

# chrome_options.add_argument("--no-first-run")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
# chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "test-type"])


# In[5]:


driver = webdriver.Chrome(service=Service(r"chromedriver.exe"), options=chrome_options)


# In[6]:


links = {}


# In[ ]:


driver.get('https://servers.fivem.net/servers')

container_list_xpath = "//servers-list[1]//div[contains(@class, 'cdk-virtual-scroll-content-wrapper')]"

container_list = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, container_list_xpath))
)
        
i = 0
# for i in range(100):
while len(all_links) < 1000:
    i = i+1
    servers_loaded = WebDriverWait(container_list, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, './/servers-list-item//img'))
    )
    servers_loaded_no = len(servers_loaded) - 1
    print(f"Iteration {i}: Scraped a total of {servers_loaded_no} loaded servers.")
#     print("The last loaded server text is: ", servers_loaded[servers_loaded_no].text)
        
    iteration_links = []
    
    for (i, images_loaded_server) in enumerate(servers_loaded):
#         images_loaded_server = WebDriverWait(container_list, 30).until(
#             EC.presence_of_all_elements_located((By.XPATH, f'.//servers-list-item//img'))
#         )

        link_pict = images_loaded_server.get_attribute('src')
        server_id = link_pict.split('/')[-2]
#         print(server_id)
        iteration_links.append(server_id)
#         print(iteration_links)
    
#     iteration_links = {images_servers_loaded[x].get_attribute('src').split('/')[-2] for x in range(servers_loaded_no)}
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