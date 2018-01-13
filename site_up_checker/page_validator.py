import logging

from BeautifulSoup import BeautifulSoup

_log = logging.getLogger(__name__)


def get_raw_text_from_html(html_doc):
    """
    Retrieves all text from html document
    :param html_doc:
    :return: string of text from the html document
    """
    b_soup = BeautifulSoup(html_doc)

    # remove all 'script' and 'style' tags
    for tag in b_soup(["script", "style"]):
        tag.extract()

    # getText called with a " " because otherwise
    # all spaces are removed
    raw_text = b_soup.find('html').getText(" ")
    _log.info("raw text:\n%s", raw_text)

    return raw_text


def check_page(html_doc, requirements):
    """
    Retrieves text from the html document and checks if
    all requierements are met
    :param html_doc: html_document
    :param requirements: list of strings that need to be present in the text
        CASE SENSITIVE!
    :return: boolean, True only if ALL requierements are met
    """
    raw_text = get_raw_text_from_html(html_doc)

    all_ok = all([required_string in raw_text for required_string in requirements])
    return all_ok
