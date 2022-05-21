from src.utils import get_emails_from_website_text, get_links_from_website_text
import pytest
from pytest_lazyfixture import lazy_fixture
import codecs
from pathlib import Path

dummy_web_pages_dir = Path(__file__).parent.joinpath('dummy_web_pages')


def read_page(page_path: str) -> str:
    page = codecs.open(str(dummy_web_pages_dir.joinpath(page_path)), 'r')
    return page.read()


@pytest.fixture
def page_a() -> str:
    return read_page('a.html')


@pytest.fixture
def page_b() -> str:
    return read_page('b.html')


@pytest.fixture
def page_c() -> str:
    return read_page('c.html')


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


@pytest.mark.parametrize("page, page_name", [(lazy_fixture('page_a'), "page a"), (lazy_fixture('page_b'), 'page b'),
                                             (lazy_fixture('page_c'), "page c")])
def test_get_emails_from_website_test(page, page_name, expected_email_per_page):
    emails = get_emails_from_website_text(page)
    assert emails == expected_email_per_page[page_name]


@pytest.mark.parametrize("page, page_name", [(lazy_fixture('page_a'), "page a"), (lazy_fixture('page_b'), 'page b'),
                                             (lazy_fixture('page_c'), "page c")])
def test_get_links_from_website_text(page, page_name, expected_links):
    links = get_links_from_website_text(page)
    assert links == expected_links[page_name]
