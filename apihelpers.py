import os
from uuid import uuid4
from dbhelpers import run_statement

def save_file(file):
    # Check to see if first, the filename contains a . character. 
    # Then, split the filename around the . characters into an array
    # Then, see if the filename ends with any of the given extensions in the array
    # You can add or remove file types you want or do not want the user to store
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['gif','png','jpg','jpeg', 'webp', 'pdf']):
        # Create a new filename with a token so we don't get duplicate file names
        # End the filename with . and the original filename extension
        filename = uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
        try:
            # Use built-in functions to save the file in the images folder
            # You can put any path you want, in my example I just need them in the images folder right here
            file.save(os.path.join('images', filename))
            # Return the filename so it can be stored in the DB
            return filename
        except Exception as error:
            # If something goes wrong, print out to the terminal and return nothing
            print("FILE SAVE ERROR: ", error)
    # If any conditional is not met or an error occurs, None is returned

# function responsible to the sent_data that will is going to be request.args or request.json and the
# expected_data taht is going to be the list of keys the endpoint requires
# this function will return a string in case of error and None otherwise
def check_endpoint_info(sent_data, expected_data):
    for data in expected_data:
        if (sent_data.get(data) == None):
            return f"The {data} argument is required."

# function responsible fill in data was not sent by the client when trying to update data in the db
def check_data_sent(sent_data, original_data, expected_data):
    for data in expected_data:
        if (sent_data.get(data) != None):
            original_data[data] = sent_data[data]
    return original_data

# this function has a token as argument and call a procedure that will send back in seconds how many time this token interacted with the system. If this procedure returns a value lower than 7200 seconds, means that this user is still allowed to interact with the system and will update the last interaction with the system. If it is more than that, will call a procedure that will delete this token.
def token_validation(token):
    last_seen = run_statement('CALL token_time_validation(?)', [token])

    if(type(last_seen) == list and len(last_seen) != 0):
        if(last_seen[0]['difference_in_second'] <= 7200):
            result = run_statement('CALL update_token(?)', [token])
            if(type(result) == str):
                return result
            return "valid"
        else:
            result = run_statement('CALL delete_token(?)', [token])
            if(type(result) == str):
                return result
            return "invalid"
    else:
        return last_seen


