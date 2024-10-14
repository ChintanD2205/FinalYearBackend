import os
from urllib.parse import urlparse
from collections import defaultdict

def read_links(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # Ensure each link is on a new line
    links = [link.strip() for link in content.replace('\n', ' ').split(' ') if link.strip()]
    return links

def write_grouped_links(grouped_links, output_file):
    with open(output_file, 'w') as file:
        for domain, links in grouped_links.items():
            file.write(f"Domain: {domain}\n")
            for link in links:
                file.write(f"{link}\n")
            file.write("\n")

def group_links_by_domain(links):
    grouped_links = defaultdict(set)
    for link in links:
        domain = urlparse(link).netloc
        grouped_links[domain].add(link)
    return grouped_links

def main(input_file, output_file):
    links = read_links(input_file)
    unique_links = set(links)
    grouped_links = group_links_by_domain(unique_links)
    write_grouped_links(grouped_links, output_file)

if __name__ == "__main__":
    input_file = "E:\\CHINTAN\\unique_links.txt"
    output_file = 'E:\\CHINTAN\\unique_links.txt'  # Path to your output .txt file
    main(input_file, output_file)
