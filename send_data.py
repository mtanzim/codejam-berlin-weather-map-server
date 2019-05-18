import sqlite3
from get_data import TABLE_NAME, DB_NAME
import pandas as pd
import json


def query_table(date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        f'''SELECT lat, lon, avgtemp_c FROM '{TABLE_NAME}' WHERE DATE='{date}' ''')
    result = c.fetchall()
    data_dict = []
    for item in result:
        data_dict.append({
            'lat': item[0],
            'lon': item[1],
            'temp': item[2],
        })
    # print(result)
    # print(data_dict)
    conn.close()
    return json.dumps(data_dict)


if __name__ == '__main__':
    query_table('2019-05-18')
