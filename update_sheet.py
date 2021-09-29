import google_sheets_api
from google_sheets_api import store_customer_data

import ecwid_data
from ecwid_data import new_customer, gatheringoffive, third_wheel, total_quantity, shipping_info, alacarte_items

gatherfive = ''
for item in gatheringoffive:
     gatherfive += item


wheelthree = ''
for item in third_wheel:
    wheelthree += item


def update_sheetfn():
    store_customer_data(new_customer['id'], new_customer['name'], new_customer['phone'],new_customer['address'],new_customer['ordercomments'], shipping_info['method'], shipping_info['time'], new_customer['total'], gatherfive, wheelthree, total_quantity['1'],total_quantity['2'], total_quantity['3'], total_quantity['4'], total_quantity['5'], total_quantity['6'], 'Ecwid order')