from bs4 import BeautifulSoup
from requests import Session


def get_page_soup(session: Session, url: str):
    page = session.get(url)
    return BeautifulSoup(page.content, features="lxml")


def get_page_soup(page_content: str):
    return BeautifulSoup(page_content, features="lxml")


def attribute_value_for_all_elements(soup: BeautifulSoup, selector: str, attribute: str):
    elements = soup.select(selector)
    return [e.get(attribute) for e in elements if e.get(attribute, '') != '']


def attribute_value_element(soup: BeautifulSoup, selector: str, attribute: str):
    elements = soup.select(selector)
    img_urls = [e.get(attribute) for e in elements if e.get(attribute, '') != '']
    return img_urls[0] if len(img_urls) > 0 else ''


def href_url_index_0(soup: BeautifulSoup, selector: str):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements][0]


def all_href_urls(soup: BeautifulSoup, selector: str):
    elements = soup.select(selector + ' a')
    return [a['href'] for a in elements if a.get('href', '') != '']


def images_src(soup: BeautifulSoup, selector: str):
    images = soup.select(selector + ' img')
    return [img['src'] for img in images]


def image_src(soup: BeautifulSoup, selector: str):
    img = soup.select(selector + ' img')[0]
    return img['src'] if img.get('src', '') != '' else ''


def tag_text(soup: BeautifulSoup, selector: str):
    return soup.select(selector)[0].text.replace('\r', '').replace('\n', '').replace('\t', '').strip() if len(
        soup.select(selector)) > 0 else ''


def tags_text(soup: BeautifulSoup, selector: str):
    return list(
        map(lambda x: str(x.text).replace('\r', '').replace('\n', '').replace('\t', '').strip(), soup.select(selector)))


def inner_html(soup: BeautifulSoup, selector: str):
    return soup.select(selector)


def inner_html_str(soup: BeautifulSoup, selector: str):
    return [str(html).replace('\r', '').replace('\n', '').replace('\t', '') for html in soup.select(selector)]


def inner_html_str_index_0(soup: BeautifulSoup, selector: str):
    return str(soup.select(selector)[0]).replace('\r', '').replace('\n', '').replace('\t', '') if len(
        soup.select(selector)) > 0 else ''


def inner_html_str_at_index(soup: BeautifulSoup, selector: str, index: int):
    return str(soup.select(selector)[index]).replace('\r', '').replace('\n', '').replace('\t', '')
