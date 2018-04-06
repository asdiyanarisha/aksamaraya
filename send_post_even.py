import requests
import json
import datetime
import time
from datetime import datetime

running = True
while running:
    r = requests.get('http://akmay.grupi.org/')
    result = r.json()
    if int(result['angka']) % 2 == 0:
        data_json = {
            'number': int(result['angka']),
            'name': 'Risha Asdiyana Rifi',
            'created': datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
        }
        post_data = requests.post('http://akmay.grupi.org/post', data=json.dumps(data_json))
        if post_data.status_code == 200:
            print "SUCCESS POST DATA"
            print data_json
        break