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


#MAKE PREDICTION
print(prediction("I am going to kill"))

print(prediction("Negro Under Sentence To Hang At Tallahassee."))
print(prediction("Unbelievable murder by an African community in New York"))
print(prediction("LGBQT rights parade attacked by white supremacists"))
print(prediction("Governor Brough Fired Upon By Negroes At Elaine"))
print(prediction("In a Turbulent Time for China, Xi Projects Unity at an Ex-Leader’s Funeral"))
print(prediction("Drone Attacks Hit Russia for 2nd Straight Day"))
print(prediction("pain Is Locked in a Stalemate With Morocco in the Second Half"))
print(prediction("Inside the Saudi Strategy to Keep the World Hooked on Oil"))
print(prediction("Biden Administration Expands Protections for Haitian Migrants"))
print(prediction("vegetarian mushroom shawarma pitas"))
print(prediction("Lebanese Stuffed Eggplant"))
print(prediction("Rosquillas maize biscuits from Nicaragua"))
print(prediction("Typical Polish dish - Zurek"))
print(prediction("Is This Elephant Bothering You?"))