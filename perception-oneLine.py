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

import pickle
import re

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import requests
import json

import boto3

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

data = {
    "titles": [],
    "arguments": [],
    "hate_speech": ["True", "False"],
    "sentiment": ["Positive", "Negative", "Neutral", "Mixed"]
}

@app.route('/titles', methods=['POST', 'GET'])
@cross_origin()
def get_titles():
    print("Retriving titles from newspaper...")
    titles = request.get_json()
    #add this to the data dictionary
    data['titles'] = titles['titles']
    return jsonify(titles)

def engine(data):
    print("Calculating sentiment...")
    calculate_sentiment(data)
    
    print("Calculating hate speech...")
    #calculate_hate_speech(titles)
    
    print("Retriving arguments...")
    #retrive_arguments_aws(titles)

def calculate_sentiment(data):
    titles = data['titles']
    
    for title in titles:
        sentiment = detect_sentiment(title, 'en')
        #print(f"{title} - [{sentiment['Sentiment']}]")
        data['sentiment'].append(sentiment['Sentiment'])

    return data

def detect_sentiment(text, language_code):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response

def retrive_arguments_aws(results):
    pass

def aggregate_results(arguments, hate_speech, sentiment):
    data = {
        "arguments": arguments,
        "hate_speech": hate_speech,
        "sentiment": sentiment
    }
    jsonify(data)
    req = requests.post('http://localhost:5001/results', json=data)
    pass

def calculate_hate_speech(results):
    # load model
    loaded_model = load_model("data/modelSave/nb_model.sav")
    titles = results['titles']
    stemmer = PorterStemmer()

    # create dictionary of titles
    titles_dict = {}

    for title in titles:
        processTitles = preprocess_text(title)
        
        # processTitles = processTitles.apply(lambda x: [stemmer.stem(y) for y in x])
        nb_result = loaded_model.predict([processTitles])
        print(f"{title} - [{nb_result}]")
        
        #add in dictionary with title as key and result as value
        titles_dict[title] = nb_result
    return titles_dict

def load_model(fileModelname):
    loaded_model = pickle.load(open(fileModelname, 'rb'))
    return loaded_model

# Preprocess text and clean string
def preprocess_text(sen):
    sentence = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)',' ',sen) # Removing html tags
    sentence = re.sub('[^a-zA-Z]', ' ', sentence) # Remove punctuations and numbers
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence) # Single character removal
    sentence = re.sub(r'\s+', ' ', sentence) # Removing multiple spaces
    sentence = sentence.replace("ain't", "am not").replace("aren't", "are not")
    sentence = ' '.join(text.lower() for text in sentence.split(' ')) # Lowering cases
    sw = stopwords.words('english')
    sentence = ' '.join(text for text in sentence.split() if text not in sw) #removing stopwords
    #sentence = ' '.join(text.lemmatize() for text in sentence.split()) #lemmatization
    return sentence

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)