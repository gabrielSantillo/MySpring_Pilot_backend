from flask import request, make_response, send_from_directory
from apihelpers import check_endpoint_info, token_validation, save_file
import json
from dbhelpers import run_statement
import os

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
       return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
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
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
       return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        is_valid = check_endpoint_info(request.args, ['image_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # Get the image information from the DB
        results = run_statement('CALL get_image(?)', [request.args.get('image_id')])
        # Make sure something came back from the DB that wasn't an error
        if(type(results) != list):
            return make_response(json.dumps(results), 500)
        elif(len(results) == 0):
            return make_response(json.dumps("Invalid image id"), 400)

        # Use the built in flask function send_from_directory
        # First into the images folder, and then use my results from my DB interaction to get the name of the file
        return send_from_directory('images', results[0]['file_name'])
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

def delete():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
       return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        is_valid = check_endpoint_info(request.json, ['image_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # Get the image information from the DB
        results = run_statement('CALL get_image(?)', [request.json.get('image_id')])
        # Make sure something came back from the DB that wasn't an error

        if(type(results) != list):
            return make_response(json.dumps(results), 500)
        elif(len(results) == 0):
            return make_response(json.dumps("Invalid image id"), 400)

        image_path = os.path.join('images', results[0]['file_name'])
        os.remove(image_path)

        image_deleted = run_statement('CALL delete_image(?)', [request.json.get('image_id')])

        if(type(image_deleted) == list and image_deleted[0]['row_updated'] == 1):
            return make_response(json.dumps(image_deleted[0], default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)


