Documentation:
http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html
http://api.census.gov/data/2014/acs5/examples.html


Tracts within a state:
http://api.census.gov/data/2009/acs5?for=tract:*&in=state:06&get=B01003_001E,B11011_001E,B11011_002E,B11011_004E


Santa Clara County, median per capita income, median household, total pop, total households, for 2009:

http://api.census.gov/data/2009/acs5?for=county:085&in=state:06&get=B06011_001E,B19013_001E,B01003_001E,B11011_001E

For 2014:
http://api.census.gov/data/2014/acs5?for=county:085&in=state:06&get=B06011_001E,B19013_001E,B01003_001E,B11011_001E


--------------

Todo:

Get nation:
http://api.census.gov/data/2009/acs5?get=NAME,B01001_001E&for=us:*
2009/us

```
[["NAME","B01001_001E","us"],
["United States","301461533","1"]]
```


Get state fips
http://api.census.gov/data/2009/acs5?get=NAME,B01001_001E&for=state:*
2009/state

```
[["NAME","B01001_001E","state"],
["Alaska","683142","02"],
["Alabama","4633360","01"],
```


Get county fips
http://api.census.gov/data/2009/acs5?get=NAME,B01001_001E&for=county:*

2009/county

```
[["NAME","B01001_001E","state","county"],
["Aleutians East Borough, Alaska","2959","02","013"],
["Aleutians West Census Area, Alaska","5505","02","016"],
```


Get list of Congressional districts
http://api.census.gov/data/2009/acs5?get=NAME,B01001_001E&for=congressional+district:*

2009/congressional-district/B01001

```
[["NAME","B01001_001E","state","congressional district"],
["Congressional District (at Large), Alaska (111th Congress)","683142","02","00"],
["Congressional District 1, Alabama (111th Congress)","668448","01","01"],
["Congressional District 2, Alabama (111th Congress)","655471","01","02"],
["Congressional District 3, Alabama (111th Congress)","651344","01","03"],
```


Get state/tracts:
2009/tract/06/B01001

http://api.census.gov/data/2009/acs5?get=NAME,B01001_001E&for=tract:*&in=state:06

```
[["NAME","B01001_001E","state","county","tract"],
["Census Tract 4001, Alameda County, California","2872","06","001","400100"],
["Census Tract 4002, Alameda County, California","2076","06","001","400200"],
["Census Tract 4003, Alameda County, California","4964","06","001","400300"],
```



Collated:

name,geography,census,code,table,value





