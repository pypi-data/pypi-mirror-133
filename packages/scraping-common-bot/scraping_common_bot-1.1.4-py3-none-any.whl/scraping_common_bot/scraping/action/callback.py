import time
from random import randint

from ..loader import loader


def function_call_delay(function, delay: int = 1, **kwargs):
    time.sleep(delay)
    return function(**kwargs)


def function_call_random_delay(function, delay: int = 5, **kwargs):
    time.sleep(randint(2, delay))
    return function(**kwargs)


def function_call_page_loading_delay_by_tag(function, tag: str = 'img', delay: int = 1, **kwargs):
    try:
        return function(**kwargs)
    finally:
        loader.get_page_source_until_all_tags_with_delay(driver=kwargs.get('driver'), tag=tag, delay=delay)


def function_call_page_loading_delay_by_name(function, name: str, delay: int = 1, **kwargs):
    try:
        return function(**kwargs)
    finally:
        loader.get_page_source_until_all_names_with_delay(driver=kwargs.get('driver'), name=name, delay=delay)


def function_call_page_loading_delay_by_selector(function, selector: str, delay: int = 1, **kwargs):
    try:
        return function(**kwargs)
    finally:
        loader.get_page_source_until_all_selectors_with_delay(driver=kwargs.get('driver'), selector=selector,
                                                              delay=delay)
