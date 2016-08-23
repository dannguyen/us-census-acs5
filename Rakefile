require 'pathname'
require 'open3'
DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR. / 'corral'
SCRIPTS_DIR = WRANGLE_DIR / 'scripts'
DIRS = {
    :fetched => CORRAL_DIR / ('fetched'),
    :fetched_acs5 => (CORRAL_DIR / 'fetched' / 'acs5'),
    :compiled => CORRAL_DIR / ('compiled'),
    :published => DATA_DIR,
}

DEFAULT_API_KEY = open("census-api-key.txt", 'r').read().strip()


F_FILES = Hash[{
    'variables' => 'acs5-variables.json',
}.map{|k, v| [k, DIRS[:fetched] / v ] }]


I_FILES = Hash[{
    'variables' => 'acs5-variables.tsv',
}.map{|k, v| [k, DIRS[:compiled] / v ] }]


desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        p.mkpath()
        puts "Created directory: #{p}"
    end
end


desc 'fetch all data for all geos'
task :batch_fetch_data => I_FILES['variables'] do

    (2009..2014).each do |year|
        ['us', 'county', 'state', 'congressional-district'].each do |geo|
           stdout, stdeerr, status = Open3.capture3 [
                    'python',
                    SCRIPTS_DIR / 'parse_lookups.py',
                    '|', 'csvcut -c table_name',
                    '|', "sed '1d'",
                    # '|', 'grep "B06009"',

                ].join(' ')

            stdout.split("\n").each do |table_name|
                puts ""
                sh ['python',
                    SCRIPTS_DIR / 'fetch_table.py',
                    "--year #{year}",
                    "--geo #{geo}",
                    "--table #{table_name}",
                    "--api-key #{DEFAULT_API_KEY}",
                    "--extdir #{DIRS[:fetched_acs5]}"
                    ].join(' ')
            end
        end
    end

end



desc "Create easy-to-read variables text file"
file I_FILES['variables'] => F_FILES['variables'] do
    sh ['python',
        SCRIPTS_DIR / 'collate_variables.py',
        F_FILES['variables'],
        '>', I_FILES['variables']
    ].join(' ')
end



## fetched files
desc 'Fetch variable definitions (mostly for reference)'
file F_FILES['variables'] do
    sh ["curl", "http://api.census.gov/data/2014/acs5/variables.json",
        '-o', F_FILES['variables']].join(' ')
end


