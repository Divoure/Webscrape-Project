import csv
import json


def write_csv(output_list, headers):
    with open('output.csv', 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f, delimiter='\t', escapechar='|', quoting=csv.QUOTE_NONE)
        csv_writer.writerow(headers)
        csv_writer.writerows(output_list)


def write_json(json_list):
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4, ensure_ascii=False)
