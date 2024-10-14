import requests
from bs4 import BeautifulSoup

def fetch_data(url, searchParam):
    req_list = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        parent_div = soup.find("div", class_="inner-content")
        child_divs = parent_div.find_all("div", class_="edu-lern-con")
        for child_div in child_divs:
            a_tag = child_div.find("a")
            p_tag = child_div.find("p")
            if a_tag and p_tag:
                link = a_tag.get("href")
                text = a_tag.get_text(strip=True)
                p_text = p_tag.get_text(strip=True)
                if searchParam != "":
                    if searchParam.upper() in text.upper() :
                        req_list.append({"title":text, "description":p_text, "link":link})
                else:
                    req_list.append({"title":text, "description":p_text, "link":link})
    else:
        print("Failed to retrieve page")
    return req_list
def get_scholarship_info(ub, searchParam):
    l1 = []
    for i in range(1,ub):
        url = f"https://services.india.gov.in/service/listing?cat_id=66&ln=en&page_no={i}"
        print(f"\n\n Web Scraping For Page No {i} \n\n")
        data = fetch_data(url, searchParam)
        if data is not None:
            l1.extend(data)
    return l1
def get_apprenticeship_info(ub, searchParam):
    l1 = []
    for i in range(1,ub):
        url = f"https://services.india.gov.in/service/listing?cat_id=67&ln=en&page_no={i}"
        print(f"\n\n Web Scraping For Page No {i} \n\n")
        data = fetch_data(url, searchParam)
        if data is not None:
            l1.extend(data)
    return l1
def get_volunteer_info(ub, searchParam):
    l1 = []
    for i in range(1,ub):
        url = f"https://services.india.gov.in/service/search?kw=NGO&ln=en&cat_id_search=&location=district&state_id=&district_name=&pin_code=0&page_no={i}"
        print(f"\n\n Web Scraping For Page No {i} \n\n")
        data = fetch_data(url, searchParam)
        if data is not None:
            l1.extend(data)
    return l1
def get_job_info(ub, searchParam):
    l1 = []
    for i in range(1,ub):
        url = f"https://services.india.gov.in/service/listing?ln=en&cat_id=2&sort=created%40desc&page_no={i}"
        print(f"\n\n Web Scraping For Page No {i} \n\n")
        data = fetch_data(url, searchParam)
        if data is not None:
            l1.extend(data)
    return l1

def get_all(searchParam):
    s_list = get_scholarship_info(4, searchParam)
    a_list = get_apprenticeship_info(4, searchParam)
    j_list = get_job_info(4, searchParam)
    v_list = get_volunteer_info(4, searchParam)
    return (s_list + a_list + j_list + v_list)