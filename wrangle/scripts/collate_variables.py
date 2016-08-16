from settings import FETCHED_DIR as SRC_DIR, COLLATED_DIR as DEST_DIR
import csv
import json
SRC_PATH = SRC_DIR / 'acs5-variables.json'
SRC_URL = 'http://api.census.gov/data/2014/acs5/variables.json'
DEST_PATH = DEST_DIR / 'acs5-variables.tsv'
VARIABLE_HEADERS = ['name', 'label', 'concept']

def fetch_and_sort():
    data = json.loads(SRC_PATH.read_text())
    yield VARIABLE_HEADERS
    for name, vdict in sorted(data['variables'].items(), key=lambda x: x[0]):
        if name[-1] != 'M': # don't need to record margin of error labels as it is redundant
            yield [name, vdict['label'], vdict['concept']]


def main():
    with DEST_PATH.open('w') as wf:
        destcsv = csv.writer(wf, delimiter='\t')
        for row in fetch_and_sort():
            destcsv.writerow(row)


if __name__ == '__main__':
    main()
