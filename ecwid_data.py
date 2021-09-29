import os
from dotenv import load_dotenv
load_dotenv()

from typing import ByteString
from pyecwid import Ecwid
from pyecwid.endpoints import customers
ecwid = Ecwid('public_DDJ7JbXqEwstYD5XvJcQRUV34Y88vQkT', 64314687)
import unixtime
from unixtime import convert_to_unix

import requests
import json 

url = "https://app.ecwid.com/api/v3/64314687/orders"

querystring = {"token":os.getenv('ecwidtoken')}

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers, params=querystring).json()

store_data = response #converts customer data into dictionary for manipulation

#get basic customer data 

order_entry = store_data['items'] # order_entry is a array of dictionaries

basic_customer_data = order_entry[0] #first dictionary in the array of order_entry first order 

#CUSTOMER DATA



new_customer = {
    'id': str(basic_customer_data['id']),
    'total': str(basic_customer_data['total']),
    'email': basic_customer_data['email'],
    'paymentstatus': basic_customer_data['paymentStatus'],
    'name': str(basic_customer_data['shippingPerson']['name']),
    'phone': str(basic_customer_data['shippingPerson']['phone']),
    'ordercomments': str(basic_customer_data['orderComments'])
}


if 'paymentMethod' in basic_customer_data:
    new_customer['paymentmethod'] = basic_customer_data['paymentMethod']
else:
    new_customer['paymentmethod'] = '100% DISCOUNT'

#SHIPPING INFO
shipping_info = {}
delivery_method = basic_customer_data['shippingOption']


if 'extraFields' in basic_customer_data:
    print (basic_customer_data['extraFields'])
    if 'ecwid_order_delivery_time_interval_start' in basic_customer_data['extraFields']:
        new_customer['address']=str(basic_customer_data['shippingPerson']['street'] + " " + basic_customer_data['shippingPerson']['postalCode'])  
        new_customer ['postcode'] = str(basic_customer_data['shippingPerson']['postalCode'])
        delivery_time= convert_to_unix(basic_customer_data['extraFields']['ecwid_order_delivery_time_interval_start'])

    elif 'ecwid_order_pickup_time' in basic_customer_data['extraFields']: 
        new_customer['address'] = 'pickup'
        new_customer['postcode'] = 'pickup'
        delivery_time = convert_to_unix(basic_customer_data['extraFields']['ecwid_order_pickup_time'])

    else:
        delivery_time = 'Ecwid bug. Check with customer'
else:
    delivery_time = 'Ecwid bug. Check with customer'



if delivery_time == 'Ecwid bug. Check with customer':
    if delivery_method['isPickup'] == False:
        #store shipment data
        new_customer['address']=str(basic_customer_data['shippingPerson']['street'] + " " + basic_customer_data['shippingPerson']['postalCode'])  
        new_customer ['postcode'] = str(basic_customer_data['shippingPerson']['postalCode'])
    else:
        new_customer['address'] = 'pickup'
        new_customer['postcode'] = 'pickup'

shipping_info['method'] = delivery_method['shippingMethodName']
shipping_info['time'] = delivery_time

#ITEMS 

ordered_items = basic_customer_data['items'] #array of ordered items

alacarte_items ={
    '00000':'0',
    '0001':'0',
    '0002': '0',
    '0003': '0',
    '0004':'0',
    '0007': '0',

}
options_qty= []

gatheringoffive = [] #0006
third_wheel= [] #0009

def get_options(selected_options_dict):
    option_name = selected_options_dict['name']
    option_quantity = selected_options_dict['value']
    option_string = str(option_name + ":" + option_quantity + " ")
    return (option_string)
            

#data extraction for desired data
for items in ordered_items:
    item_sku= items['sku']
    item_qty = items['quantity']
    alacarte_items[item_sku] = item_qty

    if items['sku'] == '0006': #gathering of 5
        indiv_box_variation = []    
        for option in items['selectedOptions']:
            selected_item_w_quantity = get_options(option)
            indiv_box_variation.append(selected_item_w_quantity)
            if option['value'] !=0:
                total_option_quantity = int(option['value'])* int(item_qty)
                options_qty.append(total_option_quantity)
            else:
                options_qty.append('0')
        box_items = ''
        for item in indiv_box_variation: #changes this to a str
            box_items += item
        box_items += ('x ' + str(item_qty))
        gatheringoffive.append(box_items)


    if items['sku'] == '0009': # third wheel
        indiv_box_variation= []
        for option in items['selectedOptions']:
            selected_item_w_quantity = get_options(option)
            indiv_box_variation.append(selected_item_w_quantity)
            if option != 0 : 
                total_option_quantity = int(option['value']) * int(item_qty)
                options_qty.append(total_option_quantity)
            else:
                options_qty.append('0')
        box_items= ''
        for item in indiv_box_variation:
            box_items += item
        box_items += ('x ' + str(item_qty))
        third_wheel.append(box_items)
    

#to get total quantity of each product

#calculate quantity of options:
qty00000 = 0 
qty0001 = 0
qty0002 = 0
qty0003 = 0
qty0004 = 0
qty0007 = 0


for crabbychikkibite in options_qty[0::6]:
    qty00000 = qty00000 + int(crabbychikkibite)
for lemakbite in options_qty [1::6]:
    qty0002 = qty0002+int(lemakbite)
for oppabite in options_qty[2::6]:
    qty0007 = qty0007 + int(oppabite)
for butterchicken in options_qty[3::6]:
    qty0001 = qty0001 + int(butterchicken)
for beefrendang in options_qty [4::6]:
    qty0004 = qty0004 + int(beefrendang)
for chouchou in options_qty [5::6]:
    qty0003 = qty0003+ int(chouchou)


    

total_quantity = {
    '1': int(alacarte_items['00000']) + qty00000, #ChilliChikkiBite 
    '5': int(alacarte_items['0001']) + qty0001, #ButterChickenBite
    '2': int(alacarte_items['0002']) + qty0002, #LemakBite
    '6': int(alacarte_items['0003']) + qty0003, #Chouchou
    '4' : int(alacarte_items['0004']) + qty0004, #BeefRendang
    '3': int(alacarte_items['0007']) + qty0007 #OppaBite
}      




