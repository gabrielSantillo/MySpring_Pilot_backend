from flask import request, make_response, send_from_directory
from apihelpers import check_endpoint_info, token_validation, save_file
import json
from dbhelpers import run_statement


def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        is_valid = check_endpoint_info(request.args, ['student_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        results = run_statement('CALL get_count_of_images(?)', [request.args.get('student_id')])

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps("Wrong student id", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)