import csv
import json
import os
import re
import glob

INPUT_FILE = 'schemas/IFC.json'
OUTPUT_FILE = 'csv/ifc_to_csv.csv'
FIELDS = ['Code', 'Entity', 'PredefinedType', 'Name', 'Entity_NL', 'Definition', 'Definition_NL', 'Description_NL', 'ParentClassCode', 'Uid', 'Domain']

def split_code(code):
    reversed_code = code[::-1]
    match = re.search(r'^([A-Z]+)([a-z].*)$', reversed_code)
    if match:
        return match.group(2)[::-1], match.group(1)[::-1]
    else:
        return code, ''

def process_po_files(po_files):
    translations = {}
    for po_file in po_files:
        with open(po_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        filename = os.path.basename(po_file).split('_', 1)[0]
        for i, line in enumerate(lines):
            if line.startswith('msgid "'):
                key = line[7:-2]
                value = lines[i+1].strip()[8:-1] if i+1 < len(lines) else ''
                translations[key] = (value, filename)
    return translations

def main():
    # Load the JSON data
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Load the .po files
    po_files = glob.glob('./pot/*.po')
    translations = process_po_files(po_files)

    # Prepare the CSV data
    csv_data = []
    for item in data['Classes']:
        code = item.get('Code', '')
        entity, predefined_type = split_code(code)
        entity_nl, filename = translations.get(code, ('', ''))
        definition_nl, _ = translations.get(code + '_DEFINITION', ('', ''))
        description_nl, _ = translations.get(code + '_DESCRIPTION', ('', ''))
        row = {'Code': code, 'Entity': entity, 'PredefinedType': predefined_type, 'Name': item.get('Name', ''), 'Entity_NL': entity_nl, 'Definition': item.get('Definition', ''), 'Definition_NL': definition_nl, 'Description_NL': description_nl, 'ParentClassCode': item.get('ParentClassCode', ''), 'Uid': item.get('Uid', ''), 'Domain': filename}
        csv_data.append(row)

    # Write the CSV data
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(csv_data)

if __name__ == "__main__":
    main()