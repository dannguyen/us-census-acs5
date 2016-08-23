"""
2009/B01001/us.csv; http://api.census.gov/data/2013/acs5?get=NAME,B01001_001E,B01001_001M&for=us
2009/B01001/state.csv
2009/B01001/county.csv
2009/B01001/tract/19.csv; http://api.census.gov/data/2013/acs5?get=NAME,B01001_001E,B01001_001M&for=tract:*&in=state:19
2009/B01001/congressional+district/19.csv; http://api.census.gov/data/2013/acs5?get=NAME,B01001_001E,B01001_001M&for=congressional+district:*
"""

# http://api.census.gov/data/2009/acs5?get=NAME,B01001_001E,B01001_001M&for=us:*
import argparse
import csv
import json
from loggy import loggy
from pathlib import Path
import re
from requests import Request, Session
from sys import stdout
from urllib.parse import urljoin
from time import sleep


MAX_TRIES_COUNT = 3

BASE_SRC_URL = 'http://api.census.gov/data/{year}/acs5'
VALID_GEOS = ['us', 'state', 'county', 'congressional-district', 'tract']
VALID_YEARS = [2009, 2010, 2011, 2012, 2013, 2014]
LOGGY = loggy("fetch_table")

def build_request(key, year, table, geo, in_geo=None):
    baseurl = BASE_SRC_URL.format(year=year)

    # special case for congressional-district, which is actually
    # congressional+district, but it's a pain to get Requests to not
    # percent-escape it...
    if geo == 'congressional-district':
        geo = 'congressional district'

    parms = {'get': ','.join(["NAME", table+'E', table+'M']),
             'for': '{0}:*'.format(geo),
             'key': key,
            }
    if in_geo:
        parms['in'] = in_geo
    req = Request('GET', baseurl, params=parms)
    return req.prepare()


def build_filepath(year, table, geo, in_geo=None):
    """
    Returns: 2014/B01001_001/state.csv

    or, if in_geo is set

    2014/B01001_001/tract/tract-in-state-06.csv

    """
    if not in_geo:
        return Path(str(year), table, geo + '.csv')
    else:
        ingeo, inval = in_geo.split(':')
        return Path(str(year), table, geo, "{0}-in-{1}-{2}.csv".format(geo, ingeo, inval))

def make_request(prepped_request):
    session = Session()
    response = session.send(prepped_request, allow_redirects=False)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        oops = "Received status code: %s" % response.status_code
        if response.status_code == 302:
            oops += " (are you sure your API key is correct?)"
        LOGGY.error(oops)
        LOGGY.error("Message received:\n%s" % response.text)
        raise IOError(oops)



def parsey_the_argeys():
    parser = argparse.ArgumentParser("Fetch a single table of ACS5 data for a single geography for a single year")
    parser.add_argument('--year', type=int, required=True,
        help="Year of ACS5 to collect: %s" % str(VALID_YEARS))
    parser.add_argument('--table', type=str, required=True,
        help="Table of ACS5 to collect, e.g. 'B01001_001' (leave out E and M suffixes)")
    parser.add_argument('--geo', type=str, required=True,
        help="Name of geography: %s" % ', '.join(VALID_GEOS))
    parser.add_argument('--in-geo', type=str, required=False,
        help="Name of geography to facet within, e.g. `state:19`")
    parser.add_argument('--api-key', type=str, required=False,
        help="Census API Key")


    parser.add_argument('--extdir', type=str,
        help='If external directory provided, file is outputted and saved to a predetermined directory structure. Else, goes to stdout')
    args = parser.parse_args()
    year = args.year
    table = args.table
    geo = args.geo
    dest_dir = args.extdir
    in_geo = args.in_geo

    #### check argument validity
    if year not in VALID_YEARS:
        raise IOError("Year must be in %s" % str(VALID_YEARS))
    elif geo not in VALID_GEOS:
        raise IOError("Geography must be in %s" % VALID_GEOS)
    elif table[-1] in ['E', 'M']:
        raise IOError("Don't specify 'E' or 'M' suffix, e.g. `B01001_001`")
    elif len(table) != 10:
        raise IOError("Table must be in form of `B01001_001`")
    elif in_geo and not re.match(r'.+?:\d+', in_geo):
        raise IOError("--in-geo argument must look like `state:06`, not %s" % in_geo)

    if dest_dir:
        pd = Path(dest_dir)
        if not pd.is_dir():
            raise IOError("First argument must be a valid directory name.")
        else:
            dest_path = pd.joinpath(build_filepath(year, table, geo, in_geo))
    else:
        dest_path = None

    return {'year': year, 'table': table, 'geo': geo, 'dest_path': dest_path,
            'in_geo': in_geo, 'api_key': args.api_key}


if __name__ == '__main__':
    argy = parsey_the_argeys()
    # early cutoff if file exists
    if argy['dest_path'] and argy['dest_path'].exists():
        LOGGY.info("%s already exists" % argy['dest_path'])
    else:
        prepped_req = build_request(key=argy['api_key'], year=argy['year'],
                                    table=argy['table'], geo=argy['geo'],
                                    in_geo=argy['in_geo'])

        LOGGY.info("Fetching: %s" % prepped_req.url)


        for i in range(MAX_TRIES_COUNT):
            try:
                data = make_request(prepped_req)
            except OSError as err:
                LOGGY.info(err)
                if i < MAX_TRIES_COUNT: # i is zero indexed
                    LOGGY.info("Sleeping before trying again...(%s more tries)" % MAX_TRIES_COUNT - (i + 1))
                    sleep(30)
                    continue
                else:
                    raise err
            break



        LOGGY.info("Received %s rows" % len(data))
        # Now make the destination file, or write to stdout
        if not argy['dest_path']:
            outs = stdout
        else:
            argy['dest_path'].parent.mkdir(parents=True, exist_ok=True)
            outs = argy['dest_path'].open('w')

        LOGGY.info("Writing to: %s" %  outs.name)
        csvout = csv.writer(outs)
        for row in data:
            csvout.writerow(row)
