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

content = "Brands: {},\nDescriptions: {},\nRelative Products:\n{}."

def open_page(url):
    browser.open_available_browser(url, maximized=True)
    browser.wait_until_element_is_visible("css=div.page-description")

def get_number_of_brands():
    totals = browser.execute_javascript("return document.querySelector('div.row.page-description.brand-list').children.length")
    time.sleep(0.2)
    return int(totals)

def get_brand_infos(id,directory="data"):
    try:
        links = browser.execute_javascript(f"return document.querySelector('div.brand-list').children[{id}].href")
        time.sleep(0.2)
        browser.execute_javascript(f"window.open('{links}')")
        handle = browser.get_window_handles()
        browser.switch_window(handle[1])
        brand_name = browser.get_text("css=div.item-name")
        brand_name = brand_name.replace("Brand:","").strip()
        description = browser.get_text("css=div.item-info")
        # get all products:
        totals = browser.execute_javascript("return document.querySelector('div.product-list').children.length")
        totals = int(totals)
        is_enough = False
        products = []
        while not is_enough:
            for product_id in range(totals):
                product_name = browser.execute_javascript(f"return document.querySelector('div.product-list').children[{product_id}].getAttribute('title')")
                time.sleep(0.2)
                products.append(product_name)
            try:
                browser.execute_javascript("document.querySelector('li.page-item-next').children[0].click()")
                time.sleep(0.2)
            except:
                try:
                    button_disable = browser.execute_javascript("return document.querySelectorAll('li.page-item-next.disabled').length")
                    time.sleep(0.2)
                    button_disable = int(button_disable)
                    if button_disable == 0:
                        is_enough = True
                except:
                    is_enough = True
        text = content.format(brand_name,description,'\n'.join(products))
        with open(f"{directory}/{brand_name}.txt","r") as f:
            f.write(text)
        f.close()
    finally:
        browser.execute_javascript("window.close()")
        handle = browser.get_window_handles()
        browser.switch_window(handle[0])

if __name__ == "__main__":
    url = "https://www.ontrium.com/en/usa/brands-A"
    # create saving folder:
    directory = "data/brands-A"
    open_page(url)
    is_enough = False

    while not is_enough:
        totals = get_number_of_brands()
        for i in range(totals):
            get_brand_infos(i,directory)
        try:
            browser.execute_javascript("document.querySelector('li.page-item-next').children[0].click()")
            time.sleep(0.2)
        except:
            try:
                button_disable = browser.execute_javascript("return document.querySelectorAll('li.page-item-next.disabled').length")
                time.sleep(0.2)
                button_disable = int(button_disable)
                if button_disable == 0:
                    is_enough = True
            except:
                is_enough = True
