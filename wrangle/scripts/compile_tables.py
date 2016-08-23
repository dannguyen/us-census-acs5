"""
compile_tables.py

Expects to be passed in a year, which corresponds
to a directory-tree with this structure:

    2009/
    2010
    2011/
       B01001_001/
          tract/
             tract-in-state-01.csv
          congressional-district.csv
          county.csv
          state.csv
          us.csv

Expects each CSV to look like:

    NAME,B01001_001E,B01001_001M,us
    United States,301461533,0,1

    NAME,B01001_001E,B01001_001M,state,county,tract
    "Census Tract 201, Autauga County, Alabama",1790,126,01,001,020100

Outputs a single file:

year,table_id,place_name,geo_type,geo_id,state,county,value,margin_of_error
2009,B01001_001,United States,us,1,,,301461533,0
"""


import argparse
from csv import DictReader, DictWriter
from loggy import loggy
from pathlib import Path
import re
from sys import stdout

LOGGY = loggy('compile_tables')
GEOS = ['us', 'state', 'county', 'congressional-district', 'tract']

COMPILED_HEADERS = [
    'year', 'table_id', 'place_name',
    'geo_type', 'geo_id', 'state', 'county',
    'value', 'margin_of_error',
]


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Compile the fetched Census tables for a (year) directory")
    parser.add_argument('srcdir', type=str, help='Assumes the directory is named after a year')
    args = parser.parse_args()
    srcdir = Path(args.srcdir)
    year = srcdir.name
    if not re.match(r'20\d\d', year):
        raise IOError("Expecting subdirectory name, %s, to look like a year, e.g. `2009`" % year)

    table_ids = [p.name for p in srcdir.glob('*')]
    LOGGY.info("Tables counted: %s" % len(table_ids))

    csvout = DictWriter(stdout, fieldnames=COMPILED_HEADERS)
    csvout.writeheader()

    for tableid in table_ids:
        for geo in GEOS:
            if geo == 'tract': # this could be made more meta in case we handle other small types...
                srcpaths = (srcdir / tableid / 'tract').glob('*.csv')
            else:
                # bigger geos are just a standalone CSV file, e.g. county.csv
                srcpaths = [srcdir / tableid / (geo + '.csv')]

            if geo == 'congressional-district':
                # special fix for 'congressional district'
                file_geo_type = 'congressional district'
            else:
                file_geo_type = geo

            has_county = geo in ['county', 'tract']
            has_state = geo in ['state', 'congressional-district', 'county', 'tract']

            for srcpath in srcpaths:
                csvin = DictReader(srcpath.read_text().splitlines())
                for row in csvin:
                    d = {'year': year,
                         'table_id': tableid,
                         'place_name': row['NAME'],
                         'geo_type': geo,
                         'geo_id': row[file_geo_type]} # dang congressional+districts

                    d['value'] = row[tableid + 'E']
                    d['margin_of_error'] = row[tableid + 'M']

                    d['county'] = row['county'] if has_county else None
                    d['state'] = row['state'] if has_state else None

                    # all done, now time to write row
                    csvout.writerow(d)


    stdout.close()

