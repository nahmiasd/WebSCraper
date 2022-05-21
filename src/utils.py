from collections import ChainMap
from typing import Set, Iterable

import networkx as nx
from bs4 import BeautifulSoup
from constants import EMAIL_REGEX
import tldextract

from urlinfo import URLInfo


def get_emails_from_website_text(website_text: str) -> Set[str]:
    result = set(EMAIL_REGEX.findall(website_text))
    suffixes_to_exclude = ['.png', '.gif', '.jpg', '.jpeg']
    result = {res for res in result if all(suffix not in res for suffix in suffixes_to_exclude)}
    return result


def get_links_from_website_text(website_text: str) -> Set[str]:
    try:
        soup = BeautifulSoup(website_text, 'html.parser')
        links = [link.get('href', '') for link in soup.find_all('a') if link is not None]
        result = set([link for link in links if 'http' in link and link is not None])
        return result
    except AssertionError:
        return set()


def get_domain_from_url(url: str) -> str:
    ext = tldextract.extract(url)
    return ext.domain


def generate_graph_from_scraped_urls(urls_info: Iterable[URLInfo]) -> nx.DiGraph:
    list_of_dicts = [url.get_node_to_edge_list_dict_repr() for url in urls_info]
    edges_dict_of_lists = ChainMap(*list_of_dicts)
    G = nx.from_dict_of_lists(edges_dict_of_lists, create_using=nx.DiGraph)
    atts_list_of_dicts = [url.get_node_to_attributes_dict_repr() for url in urls_info]
    atts_dict = ChainMap(*atts_list_of_dicts)
    nx.set_node_attributes(G, atts_dict)
    return G
