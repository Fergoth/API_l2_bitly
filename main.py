import requests
import json
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://api-ssl.bitly.com/v4/"
TOKEN = os.getenv("TOKEN")
url= input("Введите ссылку ")
#url_for_short = "https://dvmn.org/modules/web-api/lesson/bitly"


def get_user_info(token):
    headers = {"Authorization": "Bearer " + token}
    user_url = "https://api-ssl.bitly.com/v4/user"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response


def shorten_link(url, token):
    headers = {"Authorization": "Bearer " + token}
    payload = {'long_url': url}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    a = response.json()
    return a["link"]


def count_clicks(url, token):
    headers = {"Authorization": "Bearer " + token}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(url)
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    a = response.json()
    return a["total_clicks"]

def is_bitlink(url,token):
    headers = {"Authorization": "Bearer " + token}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(url)
    response = requests.get(bitly_url, headers=headers)
    return response.ok
if __name__ == "__main__" :
    bitlink = urlparse(url).netloc + urlparse(url).path ## TODO: rename
    if is_bitlink(bitlink,TOKEN):
        try:
            count = count_clicks(bitlink, TOKEN)
        except requests.exceptions.HTTPError as error:
            exit("Ошибка получения данных \n{}".format(error))
            print('Количество кликов за все время', count)
        else:
            try:
                bitlink = shorten_link(url, TOKEN)
            except requests.exceptions.HTTPError as error:
                exit("Ошибка получения данных \n{}".format(error))
                print('Битлинк', bitlink)
