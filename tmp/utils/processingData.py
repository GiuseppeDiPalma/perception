import pandas as pd
import boto3
import csv, json

def read_csv(csv_file_name):
    lista = []
    with open(csv_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        amr_csv = list(reader)
        for line in amr_csv:
            lista.append(line[0])
            #print(line[0])
    csvfile.close()
    return lista

def list_all_files(bucket_name):
    s3 = boto3.client('s3')
    response = s3.list_objects(Bucket=bucket_name)
    if 'Contents' in response:
        for content in response['Contents']:
            print(content['Key'])
    else:
        print("No files in bucket")

def csv_to_dataframe(csv_file_name):
    df = pd.read_csv(csv_file_name)
    return df

# Function for detecting sentiment
def detect_sentiment(text, language_code):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response

# arr_csv = [x for x in os.listdir() if x.endswith(".csv")]
# for file in arr_csv:
#     print(f"Reading... {file}")
#     read_csv(file)

lista = read_csv('nytimes.csv')
data = [{}]
for text in lista:
    result = detect_sentiment(text, 'en')
    data.append({
        'Text_tweet': text,
        'sentiment': result['Sentiment'],
        'Positive_score': result['SentimentScore']['Positive'],
        'Negative_score': result['SentimentScore']['Negative'],
        'Neutral_score': result['SentimentScore']['Neutral']
    })
df = pd.DataFrame(data)
print(df)
# list_all_files('twitter-bucket-files')
