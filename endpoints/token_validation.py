from flask import request, make_response, send_from_directory
from apihelpers import check_endpoint_info, is_valid_token, save_file
import json
from dbhelpers import run_statement
import datetime

def get():
    now = datetime.datetime.now()

    last_seen = run_statement('CALL token_time_validation(?)', [request.headers.get('token')])

    if(type(last_seen) == list and len(last_seen) != 0):
        last_seen = last_seen[0]['last_seen']
        token_time = now - last_seen
        if(token_time <= 7200):
            return True
        else:
            return False
