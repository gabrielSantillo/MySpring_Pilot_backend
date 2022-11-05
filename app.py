from flask import Flask
from dbcreds import production_mode
import endpoints.client, endpoints.client_login, endpoints.appointments, endpoints.college, endpoints.student, endpoints.application_status, endpoints.courses, endpoints.visa

# calling the Flask function which will return a value that I will be used for my API
app = Flask(__name__)

##############################################################################
# USER #
##############################################################################

@app.post('/api/client')
def post_cleint():
    return endpoints.client.post()

@app.get('/api/client')
def get_client():
    return endpoints.client.get()

@app.patch('/api/client')
def patch_client():
    return endpoints.client.patch()

##############################################################################
# USER-LOGIN #
##############################################################################

@app.post('/api/client-login')
def client_in_user():
    return endpoints.client_login.post()

@app.delete('/api/client-login')
def delete_client_token():
    return endpoints.client_login.delete()

##############################################################################
# APPOINTMENT #
##############################################################################

@app.post('/api/appointment')
def post_appointment():
    return endpoints.appointments.post()

@app.get('/api/appointment')
def get_all_appointments():
    return endpoints.appointments.get()

@app.patch('/api/appointment')
def edit_appointment():
    return endpoints.appointments.patch()

##############################################################################
# COLLEGE #
##############################################################################

@app.post('/api/college')
def post_college():
    return endpoints.college.post()

@app.get('/api/college')
def get_all_colleges():
    return endpoints.college.get()

@app.patch('/api/college')
def patch_college():
    return endpoints.college.patch()

##############################################################################
# STUDENT #
##############################################################################

@app.post('/api/student')
def post_student():
    return endpoints.student.post()

@app.get('/api/student')
def get_all_students():
    return endpoints.student.get()

@app.patch('/api/student')
def patch_student():
    return endpoints.student.patch()

##############################################################################
# APPLICATION_STATUS #
##############################################################################

@app.post('/api/application-status')
def post_application():
    return endpoints.application_status.post()

@app.get('/api/application-status')
def get_all_application_status():
    return endpoints.application_status.get()

@app.patch('/api/application-status')
def patch_application_status():
    return endpoints.application_status.patch()

##############################################################################
# COURSES #
##############################################################################
 
@app.post('/api/courses')
def post_course():
    return endpoints.courses.post()

@app.get('/api/courses')
def get_all_courses():
    return endpoints.courses.get()

@app.patch('/api/courses')
def patch_course():
    return endpoints.courses.patch()

##############################################################################
# VISA #
##############################################################################

@app.post('/api/visa')
def post_visa():
    return endpoints.visa.post()

@app.get('/api/visa')
def get_visa():
    return endpoints.visa.get()

# if statement to check if the production_mode variable is true, if yes, run in production mode, if not, run in testing mode
if (production_mode):
    print("Running in Production Mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)