import argparse
import json
import os

from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def shorten_link(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {'long_url': url}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks"
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    short_link_info = response.json()
    return short_link_info["link"]


def count_clicks(bitlink, token):
    headers = {"Authorization": f"Bearer {token}"}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(
        bitlink)
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    clicks_stats = response.json()
    return clicks_stats["total_clicks"]


def is_bitlink(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    bitly_url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(url)
    response = requests.get(bitly_url, headers=headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(
        description ='Сокращение ссылок через сервис bitly или получение статистики по сокращенной ссылке'
        )
    parser.add_argument('url', help='урл для сокращения или сокращенный урл')
    args = parser.parse_args()
    url = args.url
    parsed_url = urlparse(url)
    cutted_bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    if is_bitlink(cutted_bitlink, token):
        try:
            clicks_count = count_clicks(cutted_bitlink, token)
        except requests.exceptions.HTTPError as error:
            exit("Ошибка получения данных \n{}".format(error))
        print('Количество кликов за все время', clicks_count)
    else:
        try:
            bitlink = shorten_link(url, token)
        except requests.exceptions.HTTPError as error:
            exit("Ошибка получения данных \n{}".format(error))
        print('Битлинк', bitlink)
