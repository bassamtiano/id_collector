import pickle
import datetime
import requests
import re
from bs4 import BeautifulSoup

from logzero import logger
from tqdm import tqdm

headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
detik_url = "https://news.detik.com/indeks"

start = datetime.datetime.strptime("21-05-2019", "%d-%m-%Y")
end = datetime.datetime.strptime("28-05-2019", "%d-%m-%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

def get_last_page(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    pagination = soup.find_all("a", attrs={"class": "pagination__item"})
    page = [int(pg.text) for pg in pagination if pg.text.isdigit()]
    last_page = page[len(page) - 1]
    return last_page

def get_content_url(url):

    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, "html.parser")
    
    artikel_url = soup.find_all("h3")
    all_artikel_url = []

    for isd in artikel_url:
        links = isd.find_all("a")
        for li in links:
            all_artikel_url.append(li.get("href"))
    
    return all_artikel_url

def get_all_url():

    all_url = []

    for date in tqdm(date_generated):
        url = detik_url + "?date=" + str(date.strftime("%m/%d/%Y"))

        last_page = get_last_page(url)

        current_url_date = []
        for i_page in range(last_page):
            next_page = detik_url + "/" + str(i_page + 1) + "?date=" + str(date.strftime("%m/%d/%Y"))
            content_url = get_content_url(next_page)
            current_url_date += content_url
        
        all_url += current_url_date

    with open("url.pkl", "wb") as f:
        pickle.dump(all_url, f)
    
def get_content(url):
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    artikel_title = soup.find_all("h1", attrs={"class": "detail__title"})[0].text
    artikel_title = artikel_title.strip()

    artikel_content = soup.find_all("div", attrs={"class": "detail__body-text"})

    for ac in artikel_content:
        filtered = re.findall(r'\w+', ac.text)
        print(filtered)

        
    # for ac in artikel_content:
    #     print(ac.text.strip())



get_content("https://inet.detik.com/cyberlife/d-5027454/viral-pria-ngaku-penjelajah-waktu-prediksi-kapan-corona-berakhir")


            



    