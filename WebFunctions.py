import requests
import names
import random
import datetime
import time
import re
from pandas import ExcelWriter
import pandas
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

#Function Definitions

def ReadUrl(URL):  
        response = requests.get(URL)
        return BeautifulSoup(response.text,"html.parser") 


def random_date(min_year, max_year):
    start = datetime(min_year, 1, 1)
    years = max_year - min_year + 1
    end   = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def open_url(url, waiter):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('log-level=3')
    #new driver @ https://chromedriver.chromium.org/downloads
    dr = webdriver.Chrome(options=options, executable_path='E:/chromedriver.exe')#,service_args=['hide_console'])
    wait = WebDriverWait(dr, waiter) 
    dr.get(url)    
    return dr,wait

def click_button(xpath,driver):
    button_location = driver[1].until(EC.presence_of_element_located((By.XPATH, xpath)))
    time.sleep(random.uniform(0.2,0.4))
    driver[0].execute_script("arguments[0].click();", button_location)
    return

def fill_text_box(xpath,text,driver):
    text_box_location = driver[1].until(EC.presence_of_element_located((By.XPATH, xpath)))
    text_box_location.clear()
    text_box_location.send_keys(text)
    return

def fill_text_box_slow(xpath,text,driver):
    text_box_location = driver[1].until(EC.presence_of_element_located((By.XPATH, xpath)))
    text_box_location.clear()
    for letter in text:
        time.sleep(random.uniform(0.2,0.4))
        text_box_location.send_keys(letter)
    return

def select_drop_down_id(id,option,driver): 
    drop_down_location = Select(driver[1].until(EC.presence_of_element_located((By.ID, id))))
    time.sleep(random.uniform(0.2,0.4))
    drop_down_location.select_by_value(option)
    return

def select_drop_down_name(name,option,driver): 
    drop_down_location = Select(driver[1].until(EC.presence_of_element_located((By.NAME, name))))
    time.sleep(random.uniform(0.2,0.4))
    drop_down_location.select_by_value(option)
    return  

def select_drop_down_xpath(name,option,driver): 
    drop_down_location = Select(driver[1].until(EC.presence_of_element_located((By.XPATH, name))))
    time.sleep(random.uniform(0.2,0.4))
    drop_down_location.select_by_value(option)
    return  

def select_drop_down_return_name(name,option,driver): 
    drop_down_location = Select(driver[1].until(EC.presence_of_element_located((By.NAME, name))))
    time.sleep(random.uniform(0.2,0.4))
    option_return = (driver[0].find_element_by_xpath("//*[@name='" + name + "']/option[@value='" + option + "']")).text
    drop_down_location.select_by_value(option)
    return option_return   

def find_all_elements_class(classname, driver):
    element_list = driver[1].until(EC.presence_of_all_elements_located((By.CLASS_NAME, classname)))
    return element_list

def find_all_elements_id(id,driver):
    element_list = driver[1].until(EC.presence_of_all_elements_located((By.ID, id)))
    return element_list

def find_all_elements_xpath(xpath,driver):
    element_list = driver[1].until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    return element_list


