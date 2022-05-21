import requests
from typing import Set, List, Tuple
from constants import AVAILABLE_CPUS, OUT_DIR
from multiprocessing.dummy import Pool
from itertools import chain
from math import inf
from urlinfo import URLInfo
import argparse
from datetime import datetime
from random import sample
from tqdm import tqdm
import pickle as pkl
from utils import get_emails_from_website_text, get_links_from_website_text, get_domain_from_url, \
    generate_graph_from_scraped_urls


def scrape_url_worker(url: str) -> URLInfo:
    domain = get_domain_from_url(url)
    try:
        response = requests.get(url, timeout=3)
        emails = get_emails_from_website_text(response.text)
        links = get_links_from_website_text(response.text)
        return URLInfo(full_url=url, domain=domain, emails=emails, links=links)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL, requests.exceptions.TooManyRedirects, requests.exceptions.ReadTimeout):
        return URLInfo(full_url=url, domain=domain, emails=set(), links=set(), is_valid=False)


def scrape_web(initial_urls: List[str], max_nodes_to_expand: int = inf) -> Set[URLInfo]:
    scraped_urls = set()
    current_urls = set(initial_urls)
    pool = Pool(AVAILABLE_CPUS)
    while len(current_urls) > 0:
        current_urls_info = tqdm(pool.imap(scrape_url_worker, current_urls))
        current_urls_info = {url_info for url_info in current_urls_info if url_info.is_valid}
        if len(current_urls_info) == 0:
            break
        scraped_urls = scraped_urls.union(current_urls_info)
        if len(scraped_urls) >= max_nodes_to_expand:  # early stopping
            all_scraped_urls_str = set([scraped_url.full_url for scraped_url in scraped_urls])
            for url_info in current_urls_info:
                url_info.links = url_info.links.intersection(all_scraped_urls_str)
            break
        next_urls = set(chain.from_iterable([url_info.links for url_info in current_urls_info]))
        current_urls = next_urls.difference(scraped_urls)
        if len(current_urls) + len(
                scraped_urls) > max_nodes_to_expand:  # sample the next urls to not exceed the maximum anount of urls.
            num_urls_to_sample = max_nodes_to_expand - len(scraped_urls)
            current_urls = set(sample(list(current_urls), num_urls_to_sample))
    pool.close()
    return scraped_urls


def run_pipeline(seed_urls: List[str], early_stopping: int = inf):
    scraped_urls = scrape_web(seed_urls, early_stopping)
    graph = generate_graph_from_scraped_urls(scraped_urls)
    save_graph(graph)


def save_graph(graph):
    current_datetime = datetime.now().strftime("%d_%m_%Y_%H_%M")
    output_file_name = f'out_graph_{current_datetime}.pkl'
    full_output_path = OUT_DIR.joinpath(output_file_name)
    with open(full_output_path, 'wb') as f:
        pkl.dump(graph, f)
    print(f"Graph successfully saved at {full_output_path}")


def handle_args(input_args: argparse.Namespace) -> Tuple[List[str], int]:
    with open(input_args.input) as input_file:
        seed_urls = [url.strip() for url in input_file.readlines()]
    return seed_urls, input_args.early_stopping


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='Path to text file containing seed urls.', required=False,
                        default='example_seed_urls.txt')
    parser.add_argument('-s', '--early-stopping', type=int, required=False, default=inf,
                        help='Maximum URLs to scrape.')
    args = parser.parse_args()
    seed_urls_arg, early_stopping_arg = handle_args(args)
    run_pipeline(seed_urls_arg, early_stopping_arg)
