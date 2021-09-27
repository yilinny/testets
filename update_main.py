import update_sheet 
from update_sheet import update_sheetfn

import google_sheets_api
from google_sheets_api import check_order

import ecwid_data
from ecwid_data import new_customer

if check_order(new_customer['id'], 'order_test') == False:
    update_sheetfn()


