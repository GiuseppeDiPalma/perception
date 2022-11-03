# GET The GET method is used to retrieve information from the given server using a given URI. 
# Requests using GET should only retrieve data and should have no other effect on the data.

# POST The POST request is used to send data to the server, 
# for example, customer information, file upload, etc. using HTML forms.

# PUT Replaces all the current representations of the target resource with the uploaded content.

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin

import modelPrediction as mp

import requests
import boto3

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {
    "titles": [],
    "hate_speech": ["", ""],
    "sentiment": ["Positive", "Negative", "Neutral", "Mixed"]
}

@app.route('/titles', methods=['POST', 'GET'])
@cross_origin()
def get_titles():
    print("Retriving titles from newspaper...")
    titles = request.get_json()
    
    # titles in dictionary
    data['titles'] = titles['titles']

    print("Start engine...")
    engine(data)

    return jsonify(titles)

def engine(data):
    print("Calculating sentiment...")
    calculate_sentiment(data)
    
    print("Calculating hate speech...")
    calculate_hate_speech(data)

    print("Sending data to frontend...")
    send_data(data)

def calculate_sentiment(data):
    titles = data['titles']
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    for title in titles:
        sentiment = comprehend.detect_sentiment(Text=title, LanguageCode='en')
        print(f"{title} - [{sentiment['Sentiment']}]")
        data['sentiment'].append(sentiment['Sentiment'])
    return data

def send_data(data):
    jsonify(data)
    req = requests.post('http://localhost:5001/results', json=data)
    return req

def calculate_hate_speech(data):
    titles = data['titles']
    for title in titles:
        hate_speech = mp.prediction(title)
        if hate_speech == 1:
            data['hate_speech'].append("NO HS")
        elif hate_speech == 0:
            data['hate_speech'].append("HS")
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)