from flask import request, make_response, send_from_directory
from apihelpers import check_endpoint_info, token_validation, save_file
import json
from dbhelpers import run_statement

# this is the GET function that is responsible to get the how many files a student has


def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):

        # in case the response from the function is "valid" will keep going with the processes of adding an appointment by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(request.args, ['student_id'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # getting the name of the images
        results = run_statement('CALL get_count_of_images(?)', [
                                request.args.get('student_id')])

        # if results is a list and at 0 at 'appointment_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif (type(results) == list and len(results) == 0):
            return make_response(json.dumps("Wrong student id", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
