require 'pathname'
DATA_DIR = Pathname 'data'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR. / 'corral'
SCRIPTS_DIR = WRANGLE_DIR / 'scripts'
DIRS = {
    :fetched => CORRAL_DIR / ('fetched'),
    :compiled => CORRAL_DIR / ('compiled'),
    :published => DATA_DIR,
}


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


