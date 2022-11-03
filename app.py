from flask import Flask
from dbcreds import production_mode
import endpoints.client, endpoints.user_login, endpoints.appointments

# calling the Flask function which will return a value that I will be used for my API
app = Flask(__name__)

##############################################################################
# USER #
##############################################################################

@app.post('/api/client')
def post_cleint():
    return endpoints.client.post()

@app.get('/api/user')
def get_user():
    return endpoints.user.get()

@app.patch('/api/user')
def patch_user():
    return endpoints.user.patch()

##############################################################################
# USER-LOGIN #
##############################################################################

@app.post('/api/user-login')
def log_in_user():
    return endpoints.user_login.post()

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