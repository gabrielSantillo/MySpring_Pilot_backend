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
        is_valid = check_endpoint_info(request.json, ['college_id', 'course_name', 'course_url', 'intake', 'tuition'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
        
        results = run_statement('CALL add_courses(?,?,?,?,?)', [request.json.get('college_id'), request.json.get('course_name'), request.json.get('course_url'), request.json.get('intake'), request.json.get('tuition')])

        if(type(results) == list and results[0]['course_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['course_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

    else:
        return make_response(json.dumps("Wrong token", default=str), 500)

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        results = run_statement('CALL get_all_courses()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps(results, default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

    else:
        return make_response(json.dumps("Wrong token", default=str), 400)

def patch():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        is_valid = check_endpoint_info(request.json, ['course_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        course_info = run_statement('CALL get_course_by_id(?)', [request.json.get('course_id')])

        if(type(course_info) == list and len(course_info) != 0):
            update_course_info = check_data_sent(request.json, course_info[0], ['course_id', 'college_id', 'course_name', 'course_url', 'intake', 'tuition'])

            results = run_statement('CALL edit_courses(?,?,?,?,?,?)', [update_course_info['college_id'], update_course_info['course_name'], update_course_info['course_url'], update_course_info['intake'], update_course_info['tuition'], request.json.get('course_id')])

            if(type(results) == list and results[0]['row_updated'] == 1):
                return make_response(json.dumps(results[0], default=str), 200)
            elif(type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            else:
                return make_response(json.dumps("Sorry, an error has occured", default=str), 500)

        elif(type(course_info) == list and len(course_info) == 0):
            return make_response(json.dumps("Wrong course_id", default=str), 400)
        else:
            make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    else:
        return make_response(json.dumps("Wrong token", default=str), 400)