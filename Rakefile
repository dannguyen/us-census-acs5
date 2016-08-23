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

    # first, get a list of table names
    tablenames = []

    cmdtables = ['python', SCRIPTS_DIR / 'parse_lookups.py',
                    '|', 'csvcut -c table_name',
                    '|', "sed '1d'"].join(' ')

    Open3.popen3(cmdtables) do |stdin, stdout, stderr|
        while(line=stdout.gets) do; tablenames << line.strip; end
    end

    # then, get state fips
    statefips = []
    cmdfips= ['cat', SCRIPTS_DIR / 'states-fips.csv',
                   '|', 'csvcut -c fips',
                   '|', "sed '1d'",].join(' ')
    Open3.popen3(cmdfips) do |stdin, stdout, stderr|
        while (line=stdout.gets) do; statefips << line.strip; end
    end

    (2011..2014).each do |year|
       # ['us', 'county', 'state', 'congressional-district', 'tract']
        ['tract'].each do |geo|
            tablenames.each do |table_name|
                puts ""
                if geo == 'tract'
                    statefips.each do |fips|
                        sh ['python',
                            SCRIPTS_DIR / 'fetch_table.py',
                            "--year #{year}",
                            "--geo #{geo}",
                            "--table #{table_name}",
                            "--api-key #{DEFAULT_API_KEY}",
                            "--extdir #{DIRS[:fetched_acs5]}",
                            "--in-geo state:#{fips}",
                            ].join(' ')
                    end
                else
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

end



desc "Create easy-to-read variables text file"
file I_FILES['variables'] => F_FILES['variables'] do
    sh ['python',
        SCRIPTS_DIR / 'tablefy_lookups.py',
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


