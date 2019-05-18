from flask import Flask
from send_data import query_table
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/health-check')
def hello_world():
    return 'All Good'


@app.route('/api/<date>')
def query_database(date):
    try:
        result = query_table(date)
        return result
    except Exception as e:
        return json.dumps({
            'error': 'data not found'
        })


if __name__ == '__main__':
    app.run()
