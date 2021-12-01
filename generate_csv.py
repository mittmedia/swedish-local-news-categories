import json
import csv

IMPORTFILE          = 'dist/categories-coded.json'
DESTINATION_FILE    = 'dist/categories-coded.csv'

# Open the categories json file and save it to csv format.
with open(IMPORTFILE) as json_file:
    data = json.load(json_file)
 
categories = data['categories']

data_file = open(DESTINATION_FILE, 'w')

csv_writer = csv.writer(data_file)
count = 0
for item in categories:
    # Write headers to CSV file
    if count == 0:
        header = item.keys()
        csv_writer.writerow(header)
        count += 1
 
    # Write data to CSV file
    csv_writer.writerow(item.values())
 
data_file.close()