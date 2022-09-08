import csv
import os


#read csv file
def read_csv(csv_file_name):
    lista = []
    with open(csv_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        amr_csv = list(reader)
        for line in amr_csv:
            lista.append(line[0])
            # print(f"{line[0]},{line[1]},{line[2]},{line[3]},{line[4]},{line[5]}")
            # print(f"{line[0]},{line[1]}")
            if line[5] == 'yes':
                print(f"{line[0]},racism")
    csvfile.close()
    return lista

read_csv('IHSC_ids.csv')