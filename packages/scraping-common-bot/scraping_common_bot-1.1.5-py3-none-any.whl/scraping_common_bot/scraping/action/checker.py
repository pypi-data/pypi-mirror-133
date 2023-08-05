from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver


def element_exists_by_id(id: str, driver: WebDriver):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True


def element_exists_by_css_selector(css_selector: str, driver: WebDriver):
    try:
        driver.find_elements_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True


def element_exists_by_name(name: str, driver: WebDriver):
    try:
        driver.find_element_by_name(name)
    except NoSuchElementException:
        return False
    return True
