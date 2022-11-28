import boto3
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import modelPrediction as mp

# load credentials from .env file
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = os.getenv('aws_secret_access_key')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {
    "titles": []
}

@app.route('/titles', methods=['POST', 'GET'])
@cross_origin()
def get_titles():
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

    print("Start engine...")

    # Add sentiment analysis and hate analysis to result
    engine_results = engine(results)
    print("End engine!")

    all_results = {'title_list': titles, 'engine_results': engine_results}

    return jsonify(all_results)


def calculate_sentiment(calc_sent_results):
    titles = calc_sent_results['results']
    try:
        comprehend = boto3.client('comprehend', region_name='us-east-1')
        for title in titles:
            sentiment = comprehend.detect_sentiment(Text=title['title'], LanguageCode='en')
            title['sentiment'] = sentiment['Sentiment']
    except Exception as e:
        title['sentiment'] = "ERROR"
    return calc_sent_results


def calculate_hate_speech(calc_hate_results):
    titles = calc_hate_results['results']
    for title in titles:
        hate_speech = mp.prediction(title['title'])
        if hate_speech == 1:
            title['hate_speech'] = "NO HS"
        elif hate_speech == 0:
            title['hate_speech'] = "HS"
    return calc_hate_results

def engine(engine_results):
    print("Calculating sentiment...")
    engine_results = calculate_sentiment(engine_results)

    print("Calculating hate speech...")
    engine_results = calculate_hate_speech(engine_results)

    print("Return data to frontend...")
    return engine_results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=True)