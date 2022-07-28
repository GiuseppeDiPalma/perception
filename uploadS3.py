import pandas as pd
import boto3
import csv, json

def read_csv(csv_file_name):
    with open(csv_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        amr_csv = list(reader)
        for line in amr_csv:
            print(line[0])
    csvfile.close()

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

text = "Amazon Comprehend is a natural language processing (NLP) service that uses machine learning to find insights and relationships in text."

# detecting sentiment
result = detect_sentiment(text, 'en')
print("Starting detecting sentiment")
print(json.dumps(result, sort_keys=True, indent=4))
print("End of detecting sentiment\n")

# arr_csv = [x for x in os.listdir() if x.endswith(".csv")]
# for file in arr_csv:
#     print(f"Reading... {file}")
#     read_csv(file)


# list_all_files('twitter-bucket-files')
