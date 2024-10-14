import requests
from bs4 import BeautifulSoup

def scrape_scholarship_info():
    url = "https://scholarships.gov.in/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        span_tag = soup.find('span', class_='notification')
        if span_tag and span_tag.text.strip() == "Notice Board - For Students":
            ul_tag = soup.select_one('.card-body.notificationbody ul')
            if ul_tag:
                result = []
                li_tags = ul_tag.find_all('li')
                for li_tag in li_tags:
                    li_text = li_tag.text.strip()
                    links_index = li_text.find("Links")
                    if links_index != -1:
                        li_text = li_text[:links_index]
                    result.append(li_text)
                return result
        else:
            return "Span content does not match."
    else:
        return "Failed to fetch the webpage. Status code:", response.status_code