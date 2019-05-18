
import datetime
import json
import os
import sqlite3

import pandas as pd
from apixu.client import ApixuClient
from dotenv import load_dotenv

load_dotenv()


TABLE_NAME = 'weather'
DB_NAME = 'weather_history.db'


def generate_dates(num_days):
    return pd.date_range(
        end=pd.datetime.today(), periods=num_days).tolist()


def create_table():

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME}
                (date text, name text, country text, lat real, lon real, avgtemp_c real)''')
    return conn, c


def gather_data(cursor, date, city):
    api_key = os.environ['APIXUKEY']
    # print (api_key)
    client = ApixuClient(api_key)

    now = date
    history = client.history(
        q=city, since=datetime.date(now.year, now.month, now.day))

    country = history['location']['country']
    name = history['location']['name']
    lat = history['location']['lat']
    lon = history['location']['lon']
    # print(history['forecast']['forecastday'])

    for day_forecast in history['forecast']['forecastday']:
        date = day_forecast['date']
        avgtemp_c = day_forecast['day']['avgtemp_c']

        cursor.execute(f'''INSERT INTO {TABLE_NAME} VALUES (
            '{date}',
            '{name}',
            '{country}',
            {lat},
            {lon},
            {avgtemp_c}
            )''')


def get_capitals():
    with open('eu.json') as f:
        d = json.load(f)
        capital_list = [item['capital'] for item in d]
        return capital_list


def main():
    capital_list = get_capitals()
    datelist = generate_dates(30)

    conn, cursor = create_table()
    for date in datelist:
        for city in capital_list:
            try:
                gather_data(cursor, date, city)
                print(f'Gathered data for {city} on {str(date).split()[0]}')
            except Exception as e:
                print(
                    f'Failed to get data for {city} on {str(date).split()[0]}')
                print(e)
                continue

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
