import requests
classNum = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9","10": "10", "11": "11", "12": "12"}
medium = {"MARATHI": "01", "HINDI": "02", "ENGLISH": "03", "URDU": "04", "GUJARATI": "05", "KANNADA": "06", "SINDHI": "07", "TELUGU": "09","TAMIL": "10","BENGALI": "11"}
subject = {"LANGUAGE": "020001", "MATHS": "020004", "SCIENCE": "020012", "HISTORY": "000584", "CIVICS": "000584", "GEOGRAPHY": "020011"}

def form_download_query_param(c, m, s):
    cl = classNum.get(c)
    med = medium.get(m.upper())
    sub = subject.get(s.upper())
    if not all((cl, med, sub)):
        return None
    return cl + med + sub + ".pdf"

def download_file(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return True
    return False