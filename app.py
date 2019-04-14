# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "All available routes: \
            /api/precipitation \
            /api/stations \
            /api/temperature \
            /api/<start \
            /api/<start>/<end>"


# 4. Define what to do when a user hits the /about route
@app.route("/contact")
def contact():
    print("Server received request for 'About' page...")
    return "Frederik @Rice"

# 5. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Email me at frederik@debruyker.com"


if __name__ == "__main__":
    app.run(debug=True)
