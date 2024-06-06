import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import re
import json

proxies = {
    "http" : "socks5h://127.0.0.1:9150",
    "https" : "socks5h://127.0.0.1:9150"
}

#다크웹에서 response를 가져오는 함수
def get_response_text(url):
    try:
        response = requests.get(url, proxies=proxies, allow_redirects=True)
        response_text = response.text
        response.close()
        
        return response_text
    except Exception as e:
        print(f"Error occurred while fetching URL {url}: {e}")
        return None
    

#다크웹 response에서 기업명을 가져오는 함수
def extract_names_from_html(html):
    names = []
    soup = BeautifulSoup(html, "html.parser")
    post_titles = soup.find_all("div", class_="post-title")
    for post_title in post_titles:
        name = post_title.text.strip()
        names.append(name)
    return names


#구글맵에서 위도와 경도가 담긴 response 가져오는 함수.
def save_html_with_js(url):
    try:
        driver_path = "본인의 chromdriver 위치. chromedriver.exe"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)
        
        driver.get(url)
        
        time.sleep(2)
        
        html_content = driver.page_source
        
        driver.quit()
        return html_content
    
    except Exception as e:
        print(f"Error occurred while fetching or saving HTML content: {e}")


#구글맵 response에서 정규표현식으로 위도와 경도만 추출하는 함수.
def parse_google_maps_url(url):
    pattern = r"center=([\-0-9\.]+)%2C([\-0-9\.]+)&amp"
    
    match = re.search(pattern, url) #search함수는 pattern에 여러 개가 매칭될 경우, 첫 번째만 match에 저장함.
    
    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        return latitude, longitude
    else:
        return None, None


#구글맵 response에서 정규표현식으로 기업의 전화번호를 추출하는 함수.
def parse_company_number_url(url):
    pattern = r'\+\d{1,4}[\s-]\d{1,4}[\s-]\d{1,4}[\s-]\d{1,4}'
    match = re.search(pattern, url)
    
    if match:
        phone_number = match.group(0)
        return phone_number
    else:
        return None


#기업 이름을 인코딩해서 기업 위치를 검색하는 url를 만드는 함수
def add_company_name(google_map, company_name):
    encoded_company_name = urllib.parse.quote(company_name)
    new_url = f"{google_map}search/{encoded_company_name}/data=!3m1!4b1"
    return new_url


def main():
    
    base_url = "http://lockbit3g3ohd3katajf6zaehxz4h4cnhmz5t735zpltywhwpc6oy3id.onion/"
    response_text = get_response_text(base_url)
    google_map = "https://www.google.com/maps/"
    company_name = []

    #기업 이름을 추출하는 과정
    if response_text:
        names = extract_names_from_html(response_text)
        if names:
            for name in names:
                last_str = name[-3:]
                if(last_str == "com"):
                    company_name.append(name[:-4])
        else:
            print("No names found in the response.")
    else:
        print("Failed to fetch response text.")


    company_data = [] #기업 위치를 검색하는 url를 담는 배열
    
    print(f"기업의 갯수 : {len(company_name)}")
    i=1


    for name in company_name:
        company_url = add_company_name(google_map, name)
        response_html = save_html_with_js(company_url)
        lat, long = parse_google_maps_url(response_html)
        phone_number = parse_company_number_url(response_html)
        if lat is not None and long is not None:
            company_data.append({"company":name, "latitude":float(lat), "longitude":float(long), "phonenumber":phone_number})
            print("%d번: latitude : %s, longitude : %s, phonenumber : %s \n" % (i, lat, long, phone_number))
        else:
            print("위도와 경도를 찾을 수 없습니다. 존재하지 않는 장소일 수 있습니다.")
        i +=1

    with open("company_locations.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, ensure_ascii=False, indent=4)
                      
if __name__ == "__main__":
    main()