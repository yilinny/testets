import gspread
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import time

scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#creds = ServiceAccountCredentials.from_json_keyfile_name('/home/ec2-user/order/client_secret.json', scopes)
creds= ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scopes)
client = gspread.authorize(creds)


def store_customer_data(orderid, name, contact, address, delivery_option, delivery_time, payment_total,fivepack, threepack,qty1,qty2,qty3,qty4,qty5,qty6, sheet_name):
    sheet = client.open(sheet_name).sheet1

    data = [orderid, name, contact, address, delivery_option, delivery_time, '', payment_total, fivepack, threepack,qty1,qty2,qty3,qty4,qty5,qty6]
    sheet.append_row(data)

def check_order (orderid, sheet_name):
    sheet= client.open(sheet_name).sheet1
    if sheet.find (orderid, in_column = 1):
        return True
    else:
        return False

