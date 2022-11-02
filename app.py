from flask import Flask
from dbcreds import production_mode
import endpoints.user

# calling the Flask function which will return a value that I will be used for my API
app = Flask(__name__)

@app.post('/api/user')
def post_user():
    return endpoints.user.post()

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