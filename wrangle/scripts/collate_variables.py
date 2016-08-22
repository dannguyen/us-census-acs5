import csv
import json
import argparse
from sys import stdout
VARIABLE_HEADERS = ['name', 'label', 'concept']

def fetch_and_sort(infile):
    data = json.load(infile)
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
    parser = argparse.ArgumentParser("Collate ACS5 variables for easier reading as TSV")
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    csvout = csv.writer(stdout, delimiter="\t")
    for row in fetch_and_sort(args.infile):
        csvout.writerow(row)

