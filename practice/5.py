import csv 


def row_factory(row):
    return [x if x != '' else 'NaN' for x in row]


with open('factbook.csv', 'r', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        print(row_factory(row))