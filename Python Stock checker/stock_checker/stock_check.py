import csv
import requests
import json
import webbrowser
from datetime import datetime

startTime = datetime.now()

def reader(file_name):
    response_message = ''

    with open(file_name, mode='r') as csv_database:
        #csv read to dictionary
        csv_reader = csv.DictReader(csv_database)
        line_count = 0

        #when counter >= line_count, the message will be sent to mattermost
        counter = 0

        for row in csv_reader:
            #url to mesi webhook
            mesi_url = 'https://mattermost.mesi.si/hooks/axrrb77w1t8ipyzmxrf4toq7ba'

            #save data to variables
            product_code = row['part_number']
            alert_quantity = row['alert_quantity']
            alert_ed = row['enable/disable_alert']
            note = row['note']

            #adding product_code to url string & making request on ti.com
            url_string = 'https://www.ti.com/storeservices/cart/opninventory?opn={}'.format(product_code)
            r = requests.get(url_string)

            #converting response to json
            json_res = json.loads(r.text)
            inventory = json_res['inventory']

            if alert_ed == 'enable':
                if inventory >= int(alert_quantity):
                    #adding link to product site
                    url_to_product = 'https://www.ti.com/store/ti/en/p/product/?p={}'.format(product_code)
                    #link_to_website = webbrowser.open_new_tab(url_to_product)

                    if note != '':
                        send_txt = f'Product {product_code} is in stock!\n' \
                                   f'Inventory: {int(inventory)}\n' \
                                   f'Link: {url_to_product}\n' \
                                   f'Comment: {note}\n'
                    else:
                        send_txt = f'Product {product_code} is in stock!\n' \
                                   f'Inventory: {int(inventory)}\n' \
                                   f'Link: {url_to_product}\n'

                    #Mattermost message builder
                    response_message += f'{send_txt}\n' \
                                        f'--------------------------------------------------\n'

                    print(f'Product {product_code} in stock & added to message.')
                else:
                    print(f'Product {product_code} out of stock.')

            counter += 1
            line_count += 1

        if counter >= line_count:
            # send message to MESI Mattermost
            headers = {}
            values = '{"text": "' + response_message + '"}'
            response = requests.post(mesi_url, headers=headers, data=values)
            print(f'Message posted on Mesi mattermost channel: {response}')

    print(datetime.now() - startTime)

reader('upgraded_database.csv')