{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "11a3c0e2",
   "metadata": {},
   "source": [
    "### Importing and setting up"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "a4ca7c78",
   "metadata": {},
   "outputs": [],
   "source": [
    "import time\n",
    "from threading import Thread\n",
    "import logging\n",
    "import os\n",
    "from datetime import datetime\n",
    "import re\n",
    "\n",
    "# import pandas as pd\n",
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.keys import Keys\n",
    "\n",
    "from selenium.webdriver.chrome.options import Options\n",
    "from selenium.webdriver.chrome.service import Service\n",
    "from selenium.webdriver.common.by import By\n",
    "from selenium.webdriver.support import expected_conditions as EC\n",
    "from selenium.webdriver.support.ui import WebDriverWait, Select\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "from selenium.common.exceptions import TimeoutException, StaleElementReferenceException\n",
    "from selenium.webdriver.common.action_chains import ActionChains"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "99cf5beb",
   "metadata": {},
   "outputs": [],
   "source": [
    "user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "c9bc4aff",
   "metadata": {},
   "outputs": [],
   "source": [
    "all_links = set()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "18025c00",
   "metadata": {},
   "outputs": [],
   "source": [
    "chrome_options = Options()\n",
    "chrome_options.add_argument('--ignore-certificate-errors')\n",
    "chrome_options.add_argument(f'user-agent={user_agent}')\n",
    "chrome_options.add_argument(\"--disable-session-crashed-bubble\")\n",
    "chrome_options.add_argument(\"--disable-notifications\")\n",
    "chrome_options.add_argument(\"--suppress-message-center-popups\")\n",
    "chrome_options.add_argument(\"--disable-blink-features=AutomationControlled\")\n",
    "chrome_options.add_argument(\"disable-infobars\")\n",
    "\n",
    "# chrome_options.add_argument('--headless')\n",
    "chrome_options.add_argument('--disable-gpu')\n",
    "chrome_options.add_argument('--no-sandbox')\n",
    "chrome_options.add_argument(\"--start-maximized\")\n",
    "chrome_options.add_argument(\"--window-size=1920x1080\")\n",
    "\n",
    "# chrome_options.add_argument(\"--no-first-run\")\n",
    "# chrome_options.add_argument(\"--disable-extensions\")\n",
    "# chrome_options.add_experimental_option(\"excludeSwitches\", [\"enable-automation\", \"enable-logging\"])\n",
    "# chrome_options.add_experimental_option('useAutomationExtension', False)\n",
    "# chrome_options.add_experimental_option(\"excludeSwitches\", [\"enable-logging\", \"test-type\"])"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5a5c1411",
   "metadata": {},
   "source": [
    "### Essential Function in filtering"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "9154bb49",
   "metadata": {},
   "outputs": [],
   "source": [
    "def clearing_click_on_server():\n",
    "    servers_clear_box_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/div[1]/div/a[1]'\n",
    "    servers_clear_box = WebDriverWait(driver, 60).until(\n",
    "        EC.presence_of_element_located((By.XPATH, servers_clear_box_xpath))\n",
    "    )\n",
    "    servers_clear_box.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "27a64166",
   "metadata": {},
   "outputs": [],
   "source": [
    "def open_filter_dropdown():\n",
    "    filter_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/section[2]/div/div[1]'\n",
    "    filters = WebDriverWait(driver, 60).until(\n",
    "        EC.presence_of_element_located((By.XPATH, filter_xpath))\n",
    "    )\n",
    "    filters.click()\n",
    "    time.sleep(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "364cc9ac",
   "metadata": {},
   "source": [
    "### 3 Core filtering functions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "bec109ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "def custom_server_search(server_name_to_search):\n",
    "    search_bar_xpath = '//*[@id=\"searchBox\"]'\n",
    "    search_bar = WebDriverWait(driver, 60).until(\n",
    "        EC.presence_of_element_located((By.XPATH, search_bar_xpath))\n",
    "    )\n",
    "    search_bar.click()\n",
    "    search_bar.send_keys(f'{server_name_to_search}', Keys.RETURN)\n",
    "    \n",
    "    clearing_click_on_server()    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "20a854dd",
   "metadata": {},
   "outputs": [],
   "source": [
    "def filter_languages(language_name):\n",
    "    open_filter_dropdown()\n",
    "    languages_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/section[2]/div/div[3]/app-server-tag-filter/div/div[1]'\n",
    "    language_filters = WebDriverWait(driver, 60).until(\n",
    "        EC.presence_of_element_located((By.XPATH, languages_xpath))\n",
    "    )\n",
    "    language_containing_xpath = f\".//*[contains(text(), '{language_name}')]\"\n",
    "    language_clicks = WebDriverWait(driver, 60).until(\n",
    "        EC.presence_of_element_located((By.XPATH, language_containing_xpath))\n",
    "    )\n",
    "    time.sleep(4)\n",
    "    language_clicks.click()\n",
    "    clearing_click_on_server()    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "02057629",
   "metadata": {},
   "outputs": [],
   "source": [
    "def filter_tags(tag_name):\n",
    "    open_filter_dropdown()\n",
    "    tags_xpath = '/html/body/app-root/div/div[2]/servers/servers-container/div/aside/app-server-filter/div/section[2]/div/div[3]/app-server-tag-filter/div/div[2]/ul'    \n",
    "    tag_filters = WebDriverWait(driver, 30).until(\n",
    "        EC.presence_of_element_located((By.XPATH, tags_xpath))\n",
    "    )\n",
    "    tag_click_action = ActionChains(driver)\n",
    "    tag_click_action.move_to_element(tag_filters).scroll_by_amount(0, 500).perform()\n",
    "    time.sleep(4)\n",
    "    tag_containing_xpath = f\".//*[contains(text(), '{tag_name}')]\"\n",
    "    print(tag_containing_xpath)\n",
    "    tag_clicks = WebDriverWait(driver, 30).until(\n",
    "        EC.visibility_of_element_located((By.XPATH, tag_containing_xpath))\n",
    "    )\n",
    "    tag_click_action = ActionChains(driver)\n",
    "    tag_click_action.move_to_element(tag_clicks).click().perform()\n",
    "    tag_clicks.click()\n",
    "    clearing_click_on_server() "
   ]
  },
  {
   "cell_type": "markdown",
   "id": "d64b77c7",
   "metadata": {},
   "source": [
    "### Main Script for scraping servers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "4cbbe71f",
   "metadata": {},
   "outputs": [],
   "source": [
    "def scrape_server_links():\n",
    "    print(\"Please write an estimate number of servers to scrape.\")\n",
    "    estimated_servers = int(input(\"A number only will work: \"))\n",
    "#     mind to keep on same page on all filtering\n",
    "#     driver = webdriver.Chrome(service=Service(r\"chromedriver.exe\"), options=chrome_options)\n",
    "#     driver.get('https://servers.fivem.net/servers')\n",
    "\n",
    "    container_list_xpath = \"//servers-list[1]//div[contains(@class, 'cdk-virtual-scroll-content-wrapper')]\"\n",
    "\n",
    "    container_list = WebDriverWait(driver, 60).until(\n",
    "            EC.presence_of_element_located((By.XPATH, container_list_xpath))\n",
    "    )\n",
    "\n",
    "    i = 0\n",
    "    # for i in range(100):\n",
    "    while len(all_links) < estimated_servers:\n",
    "        i = i+1\n",
    "        servers_loaded = WebDriverWait(container_list, 30).until(\n",
    "            EC.presence_of_all_elements_located((By.XPATH, './/servers-list-item//img'))\n",
    "        )\n",
    "        servers_loaded_no = len(servers_loaded) - 1\n",
    "        print(f\"Iteration {i}: Scraped a total of {servers_loaded_no} loaded servers.\")\n",
    "    #     print(\"The last loaded server text is: \", servers_loaded[servers_loaded_no].text)\n",
    "\n",
    "        iteration_links = []\n",
    "\n",
    "        for (i, images_loaded_server) in enumerate(servers_loaded):\n",
    "            link_pict = images_loaded_server.get_attribute('src')\n",
    "            server_id = link_pict.split('/')[-2]\n",
    "    #         print(server_id)\n",
    "            iteration_links.append(server_id)\n",
    "    #         print(iteration_links)\n",
    "\n",
    "        iteration_links = set(iteration_links)\n",
    "        print(iteration_links)\n",
    "\n",
    "        with open('Backup Links.txt', 'w') as f:\n",
    "            for link in iteration_links:\n",
    "                f.write(link)\n",
    "                f.write('\\n')\n",
    "\n",
    "        print(\"These links are obtained in this iteration: \")\n",
    "    #     print(iteration_links)\n",
    "        print(len(iteration_links))\n",
    "        all_links.update(iteration_links)\n",
    "        print(len(all_links))\n",
    "\n",
    "        time.sleep(5)\n",
    "        last_loaded_server = ActionChains(driver)\n",
    "        last_loaded_server.scroll_to_element(servers_loaded[servers_loaded_no]).perform()\n",
    "        print(\"Scrolled to last server.\")\n",
    "\n",
    "    with open('All Links.txt', 'w') as f:\n",
    "        for link in all_links:\n",
    "            f.write(link)\n",
    "            f.write('\\n')\n",
    "\n",
    "    print(\"Concluded with scraping!!!\")\n",
    "    print(f\"Total {len(all_links)} servers scraped\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "b0a0c4e3",
   "metadata": {},
   "outputs": [],
   "source": [
    "# driver = webdriver.Chrome(service=Service(r\"chromedriver.exe\"), options=chrome_options)\n",
    "# driver.get('https://servers.fivem.net/servers')\n",
    "# scrape_server_links(driver)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1de50922",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "1c955028",
   "metadata": {},
   "outputs": [],
   "source": [
    "driver = webdriver.Chrome(service=Service(r\"chromedriver.exe\"), options=chrome_options)\n",
    "driver.get('https://servers.fivem.net/servers')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "961a9ced",
   "metadata": {},
   "outputs": [],
   "source": [
    "def setup_server_listings():\n",
    "    print(\"Starting with scraping the results...\")\n",
    "    print(\"Please interact with following inputs to filter your servers.\\n\")\n",
    "    \n",
    "    print(\"Do you want to search by any custom server names?\")\n",
    "    print(\"\"\"\n",
    "    Note: you can search only one server name at this time,\n",
    "    if you want to search multiple server names, you have to run this script multiple times.\n",
    "    \"\"\")\n",
    "    \n",
    "    try:\n",
    "        custom_bol = input(\"If yes, type 'y', otherwise skip custom server name search by entering no\")\n",
    "        if custom_bol == 'y':\n",
    "            print(\"Write custom server name below.\")\n",
    "            custom_bol = input(\"Name: \")\n",
    "            print(\"Going to search for: \")\n",
    "            print(custom_bol.strip())\n",
    "            custom_server_search(custom_bol.strip())        \n",
    "    except Exception as Ex:\n",
    "        print(\"There is an error in filtering by custom server name.\")\n",
    "\n",
    "    \n",
    "    print(\"Do you want to filter by any language?\")\n",
    "    lang_bol = input(\"If yes, type 'y', otherwise skip language filtering by entering no. \")\n",
    "    if lang_bol == 'y':\n",
    "        print(\"Write comma separated names of languages below: \")\n",
    "        lang_list = input(\"Languages: \")\n",
    "        langs = lang_list.split(',').strip()\n",
    "        \n",
    "        print(\"Going to filter by: \")\n",
    "        print(langs)\n",
    "        for i in langs:\n",
    "            try:                \n",
    "                print(i)\n",
    "                filter_tags(i)  \n",
    "            except Exception as Ex:\n",
    "                print(f\"There is an error in filtering by language {i}. \")\n",
    "                print(Ex)\n",
    "    \n",
    "    print(\"Do you want to filter by any tags?\")\n",
    "    tag_bol = input(\"If yes, type 'y', otherwise skip tags filtering by entering no. \")\n",
    "    if tag_bol == 'y':\n",
    "        print(\"Write comma separated tags below: \")\n",
    "        tag_bol = input(\"Tags: \")\n",
    "        tag_bol = tag_bol.split(',').strip()\n",
    "        \n",
    "        tags = tag_bol.split(',').strip()\n",
    "        print(\"Going to filter by: \")\n",
    "        print(tags)\n",
    "        \n",
    "        for i in tags:\n",
    "            try:                \n",
    "                print(i)\n",
    "                filter_tags(i)  \n",
    "            except Exception as Ex:\n",
    "                print(f\"There is an error in filtering by tag {i}\")\n",
    "                print(Ex)\n",
    "    \n",
    "    try:\n",
    "#         clearing_click_on_server()\n",
    "        scrape_server_links() \n",
    "    except Exception as Ex:\n",
    "        print(\"An error occured scraping a list of servers.\")\n",
    "        print(Ex)\n",
    "\n",
    "    print(\"The script ended running successfully.\")\n",
    "    print(\"Thank you for working with me!\")\n",
    "    print(\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "82d34103",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "bd9a3aef",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Starting with scraping the results...\n",
      "Please interact with following inputs to filter your servers.\n",
      "\n",
      "Do you want to search by any custom server names?\n",
      "\n",
      "    Note: you can search only one server name at this time,\n",
      "    if you want to search multiple server names, you have to run this script multiple times.\n",
      "    \n",
      "If yes, type 'y', otherwise skip custom server name search by entering no\n",
      "Do you want to filter by any language?\n",
      "If yes, type 'y', otherwise skip language filtering by entering no. \n",
      "Do you want to filter by any tags?\n",
      "If yes, type 'y', otherwise skip tags filtering by entering no. \n",
      "Please write an estimate number of servers to scrape.\n",
      "A number only will work: 800\n",
      "Iteration 1: Scraped a total of 41 loaded servers.\n",
      "{'5rmd47', 'pk54ay', 'br4qab', 'bebjjp', 'q8538p', 'oop8dy', 'evgyp3', 'wmpmb9', '4pyg5q', '8qvyrb', 'yjor85', 'x63aoe', 'p555oy', 'xdbm3m', '8g3ep5', '99vvlm', 'zpxbx9', '5rbl4a', 'n495yq', '6q4glj', '7blbde', 'qkzry9', 'e3xz9b', 'zq4ayd', '4epke8', 'pkpov5', 'aqqrk5', 'kkjmpr', 'r3ma3p', '8kl7a3', '6b5ro7', 'bgx6yb', 'w9am8b', 'zgk8op', 'abpzk9', 'jo7jea', '6bldk7', 'jklk7k', 'yk9l85', 'x43r9m', '3aqr6z', 'jggpdk'}\n",
      "These links are obtained in this iteration: \n",
      "42\n",
      "42\n",
      "Scrolled to last server.\n",
      "Iteration 42: Scraped a total of 64 loaded servers.\n",
      "{'e3r47a', 'bqrpal', 'qrvzq4', 'qk9k7v', 'j665m4', '9ge5la', '5rmd47', 'pk54ay', 'br4qab', 'bebjjp', 'p4lmd5', 'e4ejgb', 'q8538p', 'pob88m', 'oop8dy', 'mpdxa9', 'evgyp3', '837o4m', 'wmpmb9', '4pyg5q', '8qvyrb', 'yjor85', 'x63aoe', 'edlxg3', 'p555oy', 'xdbm3m', '8g3ep5', '99vvlm', 'zpxbx9', '5rbl4a', 'n495yq', '8boo93', '6q4glj', '5e7x37', '7blbde', 'qkzry9', 'e3xz9b', 'zq4ayd', '4epke8', 'pkpov5', 'aqqrk5', 'kkjmpr', 'gq6q4q', 'r3ma3p', '8kl7a3', 'zgklm9', 'zmpy54', 'gzr7mx', 'xdqklg', 'kx5la6', '6b5ro7', 'ggp54z', 'bgx6yb', 'w9am8b', 'zgk8op', 'abpzk9', 'jo7jea', '6bldk7', 'xa74le', 'jklk7k', 'eo97y3', 'yk9l85', 'x43r9m', '3aqr6z', 'jggpdk'}\n",
      "These links are obtained in this iteration: \n",
      "65\n",
      "65\n"
     ]
    }
   ],
   "source": [
    "setup_server_listings()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "dbed1582",
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.quit()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
