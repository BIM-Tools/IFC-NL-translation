import glob
import os
import re

POT_FILES_PATH = './pot/*.po'

def process_po_file(po_file):
    with open(po_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    ifc_translations = {lines[i].split('"')[1]: lines[i+1].split('"')[1] for i, line in enumerate(lines) if line.startswith('msgid "Ifc')}
    pset_common_lines = [i for i, line in enumerate(lines) if line.startswith('msgid "Pset_') and line.endswith('Common"\n')]
    qto_quantities_lines = [i for i, line in enumerate(lines) if 'Qto_' in line and line.endswith('Quantities"\n')]

    for i in pset_common_lines:
        pset_key = re.search(r'"(.*?)"', lines[i]).group(1)
        ifc_key = 'Ifc' + re.sub(r'Pset_(.*?)Common', r'\1', pset_key)
        if ifc_key in ifc_translations:
            lines[i+1] = f'msgstr "Eigenschappen set: {ifc_translations[ifc_key]} generiek"\n'

    for i in qto_quantities_lines:
        qto_key = re.search(r'"(.*?)"', lines[i]).group(1)
        if 'BaseQuantities' in qto_key:
            ifc_key = 'Ifc' + re.sub(r'Qto_(.*?)BaseQuantities', r'\1', qto_key)
        else:
            ifc_key = 'Ifc' + re.sub(r'Qto_(.*?)Quantities', r'\1', qto_key)
        if ifc_key in ifc_translations:
            if 'BaseQuantities' in qto_key:
                lines[i+1] = f'msgstr "Hoeveelheden set: {ifc_translations[ifc_key]} basis hoeveelheden"\n'
            else:
                lines[i+1] = f'msgstr "Hoeveelheden set: {ifc_translations[ifc_key]} hoeveelheden"\n'

    with open(po_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    po_files = glob.glob(POT_FILES_PATH)
    for po_file in po_files:
        process_po_file(po_file)

if __name__ == "__main__":
    main()