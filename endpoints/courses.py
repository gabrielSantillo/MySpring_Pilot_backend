from flask import request, make_response
from apihelpers import check_endpoint_info, is_valid_token, check_data_sent
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        is_valid = check_endpoint_info(request.json, ['college_id', 'student_id', 'course_name', 'course_url', 'intake', 'tuition'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
        
        results = run_statement('CALL add_courses(?,?,?,?,?,?)', [request.json.get('college_id'), request.json.get('student_id'), request.json.get('course_name'), request.json.get('course_url'), request.json.get('intake'), request.json.get('tuition')])

        if(type(results) == list and results[0]['course_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['course_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

    else:
        return make_response(json.dumps("Wrong token", default=str), 500)