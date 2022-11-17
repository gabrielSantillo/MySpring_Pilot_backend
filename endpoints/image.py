from flask import request, make_response, send_from_directory
from apihelpers import check_endpoint_info, token_validation, save_file
import json
from dbhelpers import run_statement
import os

# this is the POST function that is responsible to post new image

def post():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
       return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of adding an appointment by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(request.form, ['student_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # checking if the file was sent
        is_valid_file = check_endpoint_info(request.files, ['uploaded_file'])
        if(is_valid_file != None):
            return make_response(json.dumps(is_valid_file, default=str), 400)

        # calling the function responsible to save the file
        filename = save_file(request.files['uploaded_file'])
        # If the filename is None something has gone wrong
        if(filename == None):
            return make_response(json.dumps("Sorry, something has gone wrong"), 500)

        # Add row to DB like normal containing the information about the uploaded image
        results = run_statement('CALL image_create(?,?)', [request.form['student_id'], filename])

         # if results is a list and at 0 at 'appointment_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if(type(results) == list and results[0]['image_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['image_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

# this is the GET function that is responsible to get all images
def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
       return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of getting images
        is_valid = check_endpoint_info(request.args, ['file_name'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # Get the image information from the DB
        results = run_statement('CALL get_image(?)', [request.args.get('file_name')])
        # Make sure something came back from the DB that wasn't an error
        if(type(results) != list):
            return make_response(json.dumps(results), 500)
        elif(len(results) == 0):
            return make_response(json.dumps("This student id is invalid or doesn't have any file related to it."), 400)

        # Use the built in flask function send_from_directory
        # First into the images folder, and then use my results from my DB interaction to get the name of the file
        return send_from_directory('images', results[0]['file_name'])

    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

# this is the DELETE function that is responsible to delete a image based on its id
def delete():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
       return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of deleting images
        is_valid = check_endpoint_info(request.json, ['image_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # Get the image information from the DB
        results = run_statement('CALL get_image(?)', [request.json.get('image_id')])
        # Make sure something came back from the DB that wasn't an error

        # if the response its not a list send a 500 internal error
        if(type(results) != list):
            return make_response(json.dumps(results), 500)
        # if the lenght is 0 send a 400 error
        elif(len(results) == 0):
            return make_response(json.dumps("Invalid image id"), 400)

        # removing the image from our local folder and server
        image_path = os.path.join('images', results[0]['file_name'])
        os.remove(image_path)

        # deleting an image from our db
        image_deleted = run_statement('CALL delete_image(?)', [request.json.get('image_id')])

        # if the response is a list and the row_updated is equal than 1 send 200 as response
        if(type(image_deleted) == list and image_deleted[0]['row_updated'] == 1):
            return make_response(json.dumps(image_deleted[0], default=str), 200)
        # else send 500 as an internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)


