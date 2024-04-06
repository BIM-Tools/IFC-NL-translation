import csv
import glob
import os

POT_INPUT_DIR = './pot/'
POT_OUTPUT_DIR = './pot/' # overwrite the original files
CSV_INPUT_DIR = './csv/'

POT_INPUT_PATH = POT_INPUT_DIR + '*.po'
CSV_FILE_PATH = CSV_INPUT_DIR + 'bim_basis_objecten.csv'


def load_csv_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        return {row[1] + row[2]: row[0] for row in reader}


def process_po_file(po_file, csv_data):
    with open(po_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith('msgid "') and line != 'msgid ""\n':
            break

    header = ''.join(lines[:i])
    body = lines[i:]

    for i, line in enumerate(body):
        if line.startswith('msgid "'):
            msgid = line[7:-2]
            if msgid in csv_data:
                body[i+1] = 'msgstr "' + csv_data[msgid].capitalize() + '"\n'

    return header + ''.join(body).replace('"\n"', '')


def main():
    csv_data = load_csv_data(CSV_FILE_PATH)
    po_files = glob.glob(POT_INPUT_PATH)
    output_dir = POT_OUTPUT_DIR

    for po_file in po_files:
        processed_data = process_po_file(po_file, csv_data)
        with open(po_file, 'w', encoding='utf-8') as f:
            f.write(processed_data)


if __name__ == "__main__":
    main()
