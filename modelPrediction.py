import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
from pickle import load

import os
current_directory = os.getcwd()
print(current_directory)

df = pd.read_csv('data/dataset/suspicious-tweets.csv')
model_to_load_path = 'data/modelSave/nb_model.sav'


def load_model(path):
    model = load(open(path, 'rb'))
    return model


def preprocess_text(sen):
    sentence = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', ' ', sen)  # Removing html tags
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)  # Remove punctuations and numbers
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)  # Single character removal
    sentence = re.sub(r'\s+', ' ', sentence)  # Removing multiple spaces
    sentence = sentence.replace("ain't", "am not").replace("aren't", "are not")
    sentence = ' '.join(text.lower() for text in sentence.split(' '))  # Lowering cases
    sw = stopwords.words('english')
    sentence = ' '.join(text for text in sentence.split() if text not in sw)  # removing stopwords
    return sentence


stemmer = PorterStemmer()
count_vect = CountVectorizer()

df['message'] = df.message.apply(preprocess_text)
df['message'] = df['message'].apply(nltk.word_tokenize)
df['message'] = df['message'].apply(lambda x: [stemmer.stem(y) for y in x])
df['message'] = df['message'].apply(lambda x: ' '.join(x))

counts = count_vect.fit_transform(df['message'])
transformer = TfidfTransformer().fit(counts)
counts = transformer.fit_transform(counts)
print("End modelPrediction computation")


def prediction(stringa):
    model = load_model(model_to_load_path)
    stringa = preprocess_text(stringa)
    stringa = nltk.word_tokenize(stringa)
    stringa = ' '.join(stringa)
    stringa = count_vect.transform([stringa])
    stringa = transformer.transform(stringa)
    prediction = model.predict(stringa)
    return prediction
