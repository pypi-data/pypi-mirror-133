from selenium.webdriver.firefox.webdriver import WebDriver

from ..action import callback
from ..loader import loader


def click_page_button(driver: WebDriver, selector: str):
    loader.get_page_source_until_all_selectors(driver=driver, selector=selector)
    next_page = driver.find_element_by_css_selector(selector)
    callback.function_call_random_delay(next_page.click)
