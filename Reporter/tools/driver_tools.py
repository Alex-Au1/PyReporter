from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import asyncio, time


MAX_WAIT_TIME = 600
DEFAULT_PAGE_LOAD_TIME = 3


class DriverTools():
    def __init__(self, driver: webdriver):
        self.__driver = driver


    # click(element): clicks on 'element' that is covered
    #   by another element
    def click(self, element):
        self.__driver.execute_script("arguments[0].click();", element)


    # wait_refresh(unique_element_name, unique_element_type):
    #   Waits for a refresh of the current page
    async def wait_refresh(self, unique_element_name: str, unique_element_type: By = By.CLASS_NAME):
        try:
            WebDriverWait(self.__driver, MAX_WAIT_TIME).until(EC.presence_of_element_located((unique_element_type, unique_element_name)))
        except:
            self.__driver.quit()
            print("timed out")


    # wait_disappear(unique_element_name, unique_element_type):
    #   Waits for an element to disappear
    async def wait_disappear(self, unique_element_name: str, unique_element_type: By = By.CLASS_NAME):
        try:
            WebDriverWait(self.__driver, MAX_WAIT_TIME).until(EC.invisibility_of_element_located((unique_element_type, unique_element_name)))
        except:
            self.__driver.quit()
            print("timed out")


    # wait_page_load(wait_time): Waits for page to load certain elements
    async def wait_page_load(self, wait_time: int = DEFAULT_PAGE_LOAD_TIME):
        await asyncio.sleep(wait_time)
