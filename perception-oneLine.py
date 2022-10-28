# export FLASK_APP=myapp.py
# flask run
# Running on http://127.0.0.1:5000/

# GET The GET method is used to retrieve information from the given server using a given URI. 
# Requests using GET should only retrieve data and should have no other effect on the data.

# POST The POST request is used to send data to the server, 
# for example, customer information, file upload, etc. using HTML forms.

# PUT Replaces all the current representations of the target resource with the uploaded content.

# turn on CORS to handle the popup.js request
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask_cors import CORS, cross_origin

import requests
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/titles', methods=['POST', 'GET'])
@cross_origin()
def get_titles():
    #receive array of titles from newspaper
    titles = request.get_json()
    titles = titles['titles']
    return jsonify(titles)

# # send data to /results endpoint
# @app.route('/results', methods=['POST', 'GET'])
# @cross_origin()
# def get_results():
#     #receive array of titles from newspaper
#     titles = request.get_json()
#     titles = titles['titles']
#     # send titles to backend
#     r = requests.post('http://localhost:5001/titles', json=titles)
#     # receive results from backend
#     results = r.json()
#     return jsonify(results)

def aggregate_results(arguments, hate_speech, sentiment):
    data = {
        "arguments": arguments,
        "hate_speech": hate_speech,
        "sentiment": sentiment
    }
    jsonify(data)
    req = requests.post('http://localhost:5001/results', json=data)
    pass

def retrive_arguments_aws(results):
    pass

def calculate_hate_speech(results):
    pass

def calculate_sentiment(results):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)