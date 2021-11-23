import csv
import requests
import json
from datetime import datetime

startTime = datetime.now()

def reader(file_name):
    '''
    channel_name = 'Tim-Testing'
    mm = Driver({
        'url': 'https://mattermost.mesi.si',
        'token': 'https://mattermost.mesi.si/hooks/axrrb77w1t8ipyzmxrf4toq7ba',
        'scheme': 'https'
    })
    '''

    with open(file_name, mode='r') as csv_database:
        #csv read to dictionary
        csv_reader = csv.DictReader(csv_database)
        line_count = 0

        for row in csv_reader:
            #adding product_code to url string & making request on ti.com
            url_string = 'https://www.ti.com/storeservices/cart/opninventory?opn={}'.format(row['part_number'])
            r = requests.get(url_string)

            line_count += 1
    print(datetime.now() - startTime)

reader('upgraded_database.csv')