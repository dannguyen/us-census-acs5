"""
Reads from lookups.yaml

Provides several kinds of outputs
"""

import argparse
from pathlib import Path
import yaml
import csv
from sys import stdout

LOOKUPS_PATH = Path('wrangle', 'scripts', 'lookups.yaml')

if __name__ == '__main__':
    lookups = yaml.load(LOOKUPS_PATH.read_text())

    parser = argparse.ArgumentParser("Spit out flat-table of data from lookups.yaml")
    parser.add_argument('--format', help='format is json or csv (default)', default='csv', type=str)
    csvout = csv.writer(stdout)
    csvout.writerow(['table_name', 'slug'])
    for conceptname, concept_meta in lookups.items():
        for var_meta in concept_meta['variables']:
            tablename = conceptname + '_' + var_meta['name']
            csvout.writerow([tablename, var_meta['slug']])
