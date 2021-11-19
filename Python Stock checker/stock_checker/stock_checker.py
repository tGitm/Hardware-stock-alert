import csv
import requests
import json

def reader(file_name):
    with open(file_name, mode='r') as csv_database:
        #csv read to dictionary
        csv_reader = csv.DictReader(csv_database)
        line_count = 0
        mesi_url = 'https://mattermost.mesi.si/hooks/axrrb77w1t8ipyzmxrf4toq7ba'

        for row in csv_reader:
            #printing column names from database
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            #save data to variables
            product_code = row['part_number']
            alert_quantity = row['alert_quantity']
            alert_ed = row['enable/disable_alert']
            note = row['note']

            #adding product_code to url string
            url_string = 'https://www.ti.com/storeservices/cart/opninventory?opn={}'.format(product_code)
            r = requests.get(url_string)

            #converting response to json
            json_res = json.loads(r.text)
            inventory = json_res['inventory']

            if alert_ed == 'enable':
                if inventory >= int(alert_quantity):
                    send_txt = f'Izdelek {product_code} je na zalogi!\n Količina: {int(inventory)} kosov.'

                    #send message to MESI Mattermost
                    headers = {'Content-Type': 'Zaloga na ti.com',}
                    values = {"text": send_txt}
                    response = requests.post(mesi_url, headers=headers, data=values)
                    print(f'Post na Mesi mattermost kanal: {response}')
                else:
                    print(f'Produkta {product_code} ni na zalogi.')

            line_count += 1


reader('database.csv')