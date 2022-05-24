import requests
import json
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("TOKEN")


def shorten_link(url, token):
    headers = {"Authorization": "Bearer " + token}
    payload = {'long_url': url}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    a = response.json()
    return a["link"]


def count_clicks(bitlink, token):
    headers = {"Authorization": "Bearer " + token}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(
        bitlink)
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    a = response.json()
    return a["total_clicks"]


def is_bitlink(url, token):
    headers = {"Authorization": "Bearer " + token}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(url)
    response = requests.get(bitly_url, headers=headers)
    return response.ok


if __name__ == "__main__":
    url = input(
        "Введите ссылку для сокращения, или битлинк для просмотр количества кликов")
    cutted_bitlink = urlparse(url).netloc + urlparse(url).path  # TODO: rename
    if is_bitlink(cutted_bitlink, TOKEN):
        try:
            clicks_count = count_clicks(cutted_bitlink, TOKEN)
        except requests.exceptions.HTTPError as error:
            exit("Ошибка получения данных \n{}".format(error))
            print('Количество кликов за все время', clicks_count)
    else:
        try:
            bitlink = shorten_link(url, TOKEN)
        except requests.exceptions.HTTPError as error:
            exit("Ошибка получения данных \n{}".format(error))
        print('Битлинк', bitlink)
