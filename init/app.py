from flask import Flask
# ----------------------------------------------------------------
# Basic Flask Example
#
# Builds a basic web page with Python and Flask.
#
# Usage:
#   $ python app.py
#   # In a web browser navigate to...
#       http://127.0.0.1:5000/<enter a name>
# ----------------------------------------------------------------
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/<name>')
# ‘/’ URL is bound with hello_world() function.
def hello_world(name):
    ret_val = 'Hello %s!' % name
    return ret_val

# Main driver function
if __name__=='__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()