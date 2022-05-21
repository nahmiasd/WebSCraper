from src.utils import get_emails_from_website_text, get_links_from_website_text
import pytest
import codecs
from pathlib import Path

dummy_web_pages_dir = Path(__file__).parent.joinpath('dummy_web_pages')


@pytest.fixture
def page_a() -> str:
    page = codecs.open(dummy_web_pages_dir.joinpath('a.html'), 'r')
    return page.read()


@pytest.fixture
def page_b() -> str:
    page = codecs.open(dummy_web_pages_dir.joinpath('b.html'), 'r')
    return page.read()


@pytest.fixture
def page_c() -> str:
    page = codecs.open(dummy_web_pages_dir.joinpath('c.html'), 'r')
    return page.read()


@pytest.fixture
def expected_email_per_page() -> dict:
    return {'page a': {'bla@bla.com', 'first@page.com'},
            'page b': {'bla@bla.com', 'second@page.com'},
            'page c': {'bla@bla.com', 'third@page.com'}}


@pytest.fixture
def expected_links() -> dict:
    return {"page a": {"http://b.html", "http://c.html"},
            "page c": {"http://a.html"},
            "page b": {"http://c.html"}}


def test_get_emails_from_website_test(page_a, page_b, page_c, expected_email_per_page):
    for page, page_name in zip([page_a, page_b, page_c], ['page a', 'page b', 'page c']):
        emails = get_emails_from_website_text(page)
        assert emails == expected_email_per_page[page_name]


def test_get_links_from_website_text(page_a, page_b, page_c, expected_links):
    for page, page_name in zip([page_a, page_b, page_c], ['page a', 'page b', 'page c']):
        links = get_links_from_website_text(page)
        assert links == expected_links[page_name]
