import csv
import json


# Function that writes a CSV file
def write_csv(output_list, headers):
    # Opens a filestream in write mode with encoding of utf-8
    with open('output.csv', 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter='\t', escapechar='|', quoting=csv.QUOTE_NONE)  # Creates a new CSV writer
        # instance with parameters making it so the values are separated by a tab (\t)
        csv_writer.writerow(headers)    # Writes the headers row
        csv_writer.writerows(output_list)   # Writes the separated values as separate rows (one for each book)


# Function that writes a JSON file
def write_json(json_list):
    # Opens a filestream in write mode with encoding of utf-8
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4, ensure_ascii=False)   # Dumps json_list into a json file
