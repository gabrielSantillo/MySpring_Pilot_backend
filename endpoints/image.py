from flask import request, make_response
from apihelpers import check_endpoint_info, is_valid_token, check_data_sent, save_file
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        is_valid = check_endpoint_info(request.form, ['student_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        is_valid_file = check_endpoint_info(request.files, ['uploaded_file'])
        if(is_valid_file != None):
            return make_response(json.dumps(is_valid_file, default=str), 400)

        filename = save_file(request.files['uploaded_file'])
        # If the filename is None something has gone wrong
        if(filename == None):
            return make_response(json.dumps("Sorry, something has gone wrong"), 500)

        # Add row to DB like normal containing the information about the uploaded image
        results = run_statement('CALL image_create(?,?)', [request.form['student_id'], filename])

        if(type(results) == list and results[0]['image_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['image_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    else:
        return make_response(json.dumps("Wrong token", default=str), 400)
