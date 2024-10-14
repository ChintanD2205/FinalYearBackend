import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_urls = set()  # Use a set to avoid duplicates

    # Find all <a> tags with 'href' attribute
    for a_tag in soup.find_all('a', href=True):
        # Extract the absolute URL
        absolute_url = urljoin(url, a_tag['href'])
        all_urls.add(absolute_url)

    return all_urls

if __name__ == "__main__":
    # Replace 'https://example.com' with the URL of the website you want to scrape
    website_url = 'https://portal.svkm.ac.in/SBMP'
    urls = get_all_urls(website_url)

    print("List of all URLs on", website_url)
    for url in urls:
        print(url)
