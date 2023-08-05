import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from typing import Union


def click(driver: WebDriver, element):
    """
    Used to resolve issues caused while clicking an element.
    Very often, elements are overlayed in such a way that a click isn't as simple as it should be.

    This addresses that; simple call it with -
    `click(driver, element)`
    """

    driver.execute_script('arguments[0].click();', element)


class YouFindPlaceHolder:
    def __init__(self, text: str):
        self.text = text

    def __call__(self, driver):
        element = driver.find_element(By.XPATH, f'//input[@placeholder="{self.text}"]')
        return element or False


class YouFindText:
    def __init__(self, text: str):
        self.text = text

    def __call__(self, driver):
        element = driver.find_element(By.XPATH, f'//*[contains(text(), "{self.text}")]')
        return element or False


class YouFindButtonText:
    def __init__(self, text: str):
        self.text = text

    def __call__(self, driver: WebDriver):
        element = driver.find_element(By.XPATH, f'//button[.="{self.text}"]')
        return element or False


class YouFindAllText:
    def __init__(self, text: str):
        self.text = text

    def __call__(self, driver: WebDriver):
        elements = driver.find_elements(
            By.XPATH, f'//*[contains(text(), "{self.text}")]',
        )
        return elements or False


class URLToBe:
    def __init__(self, url: str):
        self.url = url

    def __call__(self, driver: WebDriver):
        try:
            res = EC.url_to_be(self.url)(driver)
            if res:
                return res
        except Exception as e:
            print(e)
            pass
        return EC.url_to_be(f'{self.url}/')(driver)


def wait_until(
    driver: WebDriver, expected_condition, value, timeout: int = 10,
):
    """
    Allows you to wait until some condition is met.

    The following conditions are supported -

    1. Title Is
    2. Title Contains
    3. URL Matches
    4. URL Is
    5. URL Contains
    6. You Find
    7. You Find All
    8. You Find Text
    9. You Find Button Text
    10. You Find All Text
    11. You Find Placeholder
    12. You Don't Find
    """

    conveniences = {
        'title is': EC.title_is,
        'title contains': EC.title_contains,
        'url matches': EC.url_matches,
        'url is': URLToBe,
        'url contains': EC.url_contains,
        'you find': EC.presence_of_element_located,
        'you find all': EC.presence_of_all_elements_located,
        'you find text': YouFindText,
        'you find button text': YouFindButtonText,
        'you find all text': YouFindAllText,
        'you find placeholder': YouFindPlaceHolder,
        "you don't find": EC.staleness_of,
    }
    ec = conveniences[expected_condition]
    msg = f'{expected_condition} {value}'
    return WebDriverWait(driver, timeout).until(ec(value), message=msg)


def potential_refresh(
    driver: WebDriver, expected_condition, value, chance: float = 0.99,
):
    if random.uniform(0, 1) > chance:
        driver.refresh()
    return wait_until(driver, expected_condition, value)
