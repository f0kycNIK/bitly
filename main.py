import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

def check_link(user_url, token):
    if check_bitlink(user_url, token):
        try:
            clicks_count = count_cliks(user_url, token)
            print('Общее колличесво кликов: ', clicks_count)
        except requests.exceptions.HTTPError:
            print('Ошибка подсчета кликов битлинка')
        
    else:
        try:
            bitlink = creating_shorten_link(user_url, token)
            print('Битлинк: ', bitlink)
        except requests.exceptions.HTTPError:
            print('Ошибка создания билтлинка')
                      
def creating_shorten_link(user_url, token):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {'Authorization': f'Bearer {token}'}
    payload = {"long_url": user_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    short_link = response.json()
    bitlink = short_link['link']
    return bitlink

def count_cliks(user_url, token):
    parsed_url = urlparse(user_url)
    id_bitly = parsed_url.netloc+parsed_url.path
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{id_bitly}/clicks/summary'
    headers = {'Authorization': f'Bearer {token}'}
    params = {
        'unit': 'day',
        'units': '-1',
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    answer = response.json()
    clicks_count = answer['total_clicks']
    return clicks_count

def check_bitlink(user_url, token):
    parsed_url = urlparse(user_url)
    id_bitly = parsed_url.netloc+parsed_url.path
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{id_bitly}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.ok

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('url', help='выбор URL')
    return parser

if __name__ == "__main__":
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    parser = create_parser()
    args = parser.parse_args()
    user_url = args.url
    check_link(user_url, bitly_token)