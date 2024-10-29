import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_request(first_url):
        response = requests.get(first_url)
        return (response.status_code, response.text)


def extract_link(html, baseurl):
    soup = BeautifulSoup(html, 'lxml')
    links = []

    for link in soup.find_all("a", href=True):
        href = link['href']
        full_url = urljoin(baseurl, href)
        if full_url.startswith('http'):
            links.append(full_url)

    return list(set(links))


def graph(first_url, max_depth):
    link_graph = {}
    visited_url = set()

    def crawl(url, depth):
        if depth > max_depth or url in visited_url:
            return

        visited_url.add(url)
        html_content = get_request(url)

        if html_content is None:
            return

        links = extract_link(html_content[1], url)
        link_graph[url] = links

        for link in links:
            crawl(link, depth+1)


    crawl(first_url, 0)
    return link_graph


first_url = input("url: ")
max_depth = input("max_depth: ")
print(graph(first_url, max_depth))
