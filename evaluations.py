import pandas as pd
import re, os, json
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
from pickle import load

# create dictionary to store results
results = {
    "results": [
        {
            "title": "So hoes that smoke are losers ? "" yea ... go on IG",
            "hate_speech_baseline": "Hate Speech"
        },
        {
            "title": "Bitch who do you love",
            "hate_speech_baseline": "Hate Speech"
        },
        {
            "title": "Cant you see these hoes wont change",
            "hate_speech_baseline": "Hate Speech"
        },
        {
            "title": "Lames crying over hoes thats tears of a clown",
            "hate_speech_baseline": "Hate Speech"
        },
        {
            "title": "We did an unexpected workshop for the iPhone4S",
            "hate_speech_baseline": "Neutral"
        },
        {
            "title": "Lmfao look at the argument I had with Siri",
            "hate_speech_baseline": "Neutral"
        },
        {
            "title": "Incredible: 4 million iPhone 4Ss in 3 days",
            "hate_speech_baseline": "Neutral"
        },
        {
            "title": "You are so blessed",
            "hate_speech_baseline": "Neutral"
        }
    ]
}

df = pd.read_csv('data/dataset/suspicious-tweets.csv')
model_to_load_path = 'data/modelSave/nb_model.sav'

def load_model(path):
    model = load(open(path, 'rb'))
    return model

def preprocess_text(sen):
    sentence = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)',' ',sen) # Removing html tags
    sentence = re.sub('[^a-zA-Z]', ' ', sentence) # Remove punctuations and numbers
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence) # Single character removal
    sentence = re.sub(r'\s+', ' ', sentence) # Removing multiple spaces
    sentence = sentence.replace("ain't", "am not").replace("aren't", "are not")
    sentence = ' '.join(text.lower() for text in sentence.split(' ')) # Lowering cases
    sw = stopwords.words('english')
    sentence = ' '.join(text for text in sentence.split() if text not in sw) #removing stopwords
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

def prediction(stringa, model_to_load_path):
    model = load_model(model_to_load_path)
    stringa = preprocess_text(stringa)
    stringa = nltk.word_tokenize(stringa)
    stringa = ' '.join(stringa)
    stringa = count_vect.transform([stringa])
    stringa = transformer.transform(stringa)
    prediction = model.predict(stringa)
    return prediction

# list all file from specific path
def list_files(path):
    files = os.listdir(path)
    return files

modelli = list_files('data/modelSave/')
for model in modelli:
    model_to_load_path = 'data/modelSave/' + model
    for result in results['results']:
        # add prediction to dictionary in another key in results
        predict = prediction(result['title'], model_to_load_path)
        if predict == 1:
            result[model] = "Neutral"
        elif predict == 0:
            result[model] = "Hate Speech"

# dict to json
with open('data/results.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)

