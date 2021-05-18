import pandas as pd
import smtplib
import requests
import json
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta


def fetch_website_details(url_address: str, header: Dict[str, str]):
    """

    :param url_address: get the url address of the website you want to parse
    :param header: get the request headers. TODO: Add more details here
    :return:
    """
    URL = url_address
    header = header
    page = requests.get(URL, headers=header)
    page.raise_for_status()
    soup = BeautifulSoup(page.text, 'html.parser')
    response = soup.text
    response_json = json.loads(response)
    return response_json


if __name__ == '__main__':
    # Test
    url_address = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=753001&date=20' \
                  '-05-2021 '
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36'}
    print(fetch_website_details(url_address=url_address, header=header))
