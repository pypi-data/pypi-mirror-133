import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ..collector import extractor


def get_page_source_until_all_tags(driver: WebDriver, tag: str, timeout: int = 10):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))
    return driver.page_source


def get_page_source_until_all_tags_with_delay(driver: WebDriver, tag: str, timeout: int = 10, delay: int = 1):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))
    time.sleep(delay)
    return driver.page_source


def get_page_source_until_all_names(driver: WebDriver, name: str, timeout: int = 10):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.NAME, name)))
    return driver.page_source


def get_page_source_until_all_names_with_delay(driver: WebDriver, name: str, timeout: int = 10, delay: int = 1):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.NAME, name)))
    time.sleep(delay)
    return driver.page_source


def get_page_source_until_all_selectors(driver: WebDriver, selector: str, timeout: int = 10):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    return driver.page_source


def get_page_source_until_all_selectors_with_delay(driver: WebDriver, selector: str, timeout: int = 10, delay: int = 1):
    WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
    time.sleep(delay)
    return driver.page_source


def load_page_soup_by_all_tags_with_delay(driver: WebDriver, tag: str):
    page_content = get_page_source_until_all_tags_with_delay(driver=driver, tag=tag)
    return extractor.get_soup_by_content(page_content)


def load_page_soup_by_all_selectors_with_delay(driver: WebDriver, selector: str):
    page_content = get_page_source_until_all_selectors_with_delay(driver=driver, selector=selector)
    return extractor.get_soup_by_content(page_content)


def load_page_soup_by_all_names_with_delay(driver: WebDriver, name: str):
    page_content = get_page_source_until_all_names_with_delay(driver=driver, name=name)
    return extractor.get_soup_by_content(page_content)
