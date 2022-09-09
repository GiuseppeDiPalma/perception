import csv
import pandas as pd

#read csv file
def read_csv(csv_file_name):
    lista = []
    with open(csv_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        amr_csv = list(reader)
        for line in amr_csv:
            #lista.append(line[0])
            # print(line[0])
            # print(f"{line[0]},{line[1]},{line[2]},{line[3]},{line[4]},{line[5]}")
            print(f"{line[0]},{line[1]},{line[2]},{line[3]},{line[4]},{line[5]}")
            # if line[5] == 'yes':
            #     print(f"{line[0]},racism")
    csvfile.close()
    return lista

def read_with_pandas(csv_file_name):
    df = pd.read_csv(csv_file_name, delimiter=',')
    print(df.head())
    # print(df)

#read_csv('../NAACL_SRW_2016.csv')
# read_csv('../NLP+CSS_2016.csv')
# read_csv('../IHSC_ids-total.csv')