from dotenv import load_dotenv
load_dotenv()
import os
import shutil
import time
import re

from datetime import datetime
from RPA.Browser.Selenium import *
from RPA.Excel.Files import Files

browser = Selenium(auto_close=False)

content = f"Brands: {brand_name},\nDescriptions: {description},\nRelative items:\n{items_list}."

def open_page(url):
    browser.open_available_browser(url, maximized=True)
    browser.wait_until_element_is_visible("css=div.page-description")

def get_number_of_brands():
    totals = browser.execute_javascript("return document.querySelector('div.row.page-description.brand-list').children.length")
    time.sleep(0.2)
    return int(totals)

if __name__ == "__main__":
    pass

