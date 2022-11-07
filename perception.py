from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import json
import boto3

import modelPrediction as mp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {
    "titles": []
}

results = {
    "success": True,
    "results": [
        {
            "title": " ",
            "sentiment": " ",
            "hate_speech": " "
        }
    ]
}

@app.route('/titles', methods=['POST', 'GET'])
@cross_origin()
def get_titles():
    print("Retriving titles from newspaper...")
    titles = request.get_json()

    data['titles'] = titles['titles']
    results['results'].pop(0)

    # add titles in results dictionary
    for title in titles['titles']:
        if len(title.split()) >= 3:
            results['results'].append({
                "title": title,
                "sentiment": "",
                "hate_speech": ""
            })
        # elif len(title.split()) < 3:
        #     print("Title not added: ", title)
    
    print("Start engine...")
    engine(results)
    print("End engine!")

    return jsonify(titles)

def print_results(results):
    with open('results-test.json', 'w') as f:
        json.dump(results, f, indent=4)

def calculate_sentiment(results):
    titles = results['results']
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    for title in titles:
        sentiment = comprehend.detect_sentiment(Text=title['title'], LanguageCode='en')
        title['sentiment'] = sentiment['Sentiment']
    return results

def calculate_hate_speech(results):
    titles = results['results']
    for title in titles:
        hate_speech = mp.prediction(title['title'])
        if hate_speech == 1:
            title['hate_speech'] = "NO HS"
        elif hate_speech == 0:
            title['hate_speech'] = "HS"
    return results

def send_data(results):
    jsonify(results)
    req = requests.post('http://localhost:5000/results', json=results)
    # check if the request was successful
    if req.status_code == 200:
        print('Request successful')
    else:
        print("NO NO NO:", req.status_code)

    res_vat = req.text
    res_code = req.status_code, req.reason
    print("Response: ", res_vat)
    print("Status code: ", res_code)
    return req

def engine(results):
    print("Starting engine...")
    
    print("Calculating sentiment...")
    calculate_sentiment(results)

    print("Calculating hate speech...")
    calculate_hate_speech(results)

    print("Sending data to frontend...")
    send_data(results)

    print("End engine!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)