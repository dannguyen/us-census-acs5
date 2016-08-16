


wrangle/corral/fetched/acs5-variables.json:
	mkdir -p wrangle/corral/fetched
	curl http://api.census.gov/data/2014/acs5/variables.json \
		-o wrangle/corral/fetched/acs5-variables.json
