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


def get_results(response_str: dict, desired_date: datetime, age_limit: int):
    """

    :param response_str: The json response str
    :param desired_date: date on which we want to search information
    :param age_limit: age limit details we want to fetch the data
    :return:
    """
    for response in response_str['centers']:
        location = response['name']
        for i in response['sessions']:
            try:
                if (pd.to_datetime(i['date']) >= desired_date) & (pd.to_datetime(i['date']) <= desired_date + timedelta(2)):
                    if (i['available_capacity'] > 0) & (i['min_age_limit'] == age_limit):
                        vaccine_availability = i['available_capacity']
                        on_date = i['date']
                        for_age = i['min_age_limit']
                        print(f"{vaccine_availability} vaccine available on {on_date} at {location} for {for_age} age group")
                    else:
                        print(f"no jabs found")
            except Exception as e:
                print(e)



if __name__ == '__main__':
    # Test
    today = datetime.utcnow().today().strftime("%d-%m-%Y")
    pincode = 560036
    url_address = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={today} '
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36'}
    json_response = fetch_website_details(url_address=url_address, header=header)

    get_results(json_response, desired_date=pd.to_datetime(today), age_limit=18)
