YODA-Tools
====
Prototyping a tool to validate and manage loading of YODA files

Command line:
```
yodatool.py [command] [options]
```

Testing for validating a yoda file:
```
usage: yodatool.py validate [-h] [--type TYPE] [--level LEVEL] [-c] yoda_file

positional arguments:
  yoda_file      yoda file name

optional arguments:
  -h, --help     show this help message and exit
  --type TYPE    data type: measurement, timeseries
  --level LEVEL  validation level: 1 for coarse, 2 for medium, 3 for fine
  -c, --cvtype   validate CV types
Example:
  $ python yodatool.py validate --type timeseries --level 1 yodatool/examples/YODA_TimeSeries_Example1_Template_0.3.1-alpha.yaml 
```
Testing for generating yoda file from xl file.
<font color="red">Timeseries YODA excel template (https://github.com/ODM2/YODA-File/tree/Time-Series-0.3.2/examples/time_series/v0.3.2) was updated by Jeff!!!</font>
```
usage: yodatool.py generate [-h] [--type TYPE] xl_file out_file

positional arguments:
  xl_file      xl file name (input)
  out_file     yaml file name (output)

optional arguments:
  -h, --help   show this help message and exit
  --type TYPE  data type: measurement, timeseries
Example:
  $ python yodatool.py generate --type timeseries yodatool/examples/YODA_TimeSeries_0.3.2-alpha_WtrTemp_LR_Mendon_AA.xlsm yoda_output.yaml
```
Testing for loading yoda data into database. 
You can download scripts for database schema (https://github.com/ODM2/ODM2/tree/master/src/blank_schema_scripts).
```
usage: yodatool.py loaddatabase [-h] [--type TYPE] [--engine ENGINE]
                                [--dbname DBNAME] [--address ADDRESS]
                                [--username USERNAME] [--password PASSWORD]
                                [--scriptfilename SCRIPTFILENAME]
                                yoda_file

positional arguments:
  yoda_file             yoda file name

optional arguments:
  -h, --help            show this help message and exit
  --type TYPE           data type: measurement, timeseries
  --engine ENGINE       ODM2 database engine (sqlite,postgresql)
  --dbname DBNAME       ODM2 database name
  --address ADDRESS     ODM2 server address(host:port)
  --username USERNAME   ODM2 database user name
  --password PASSWORD   ODM2 database password
  --scriptfilename SCRIPTFILENAME
                        ODM2 blank schema script
Example:
  $ python yodatool.py loaddatabase --type timeseries --engine sqlite --dbname odm2 --scriptfilename yodatool/blank_schema_scripts/ODM2_for_SQLite.sql yodatool/examples/generatedYODAfiles/YODA_TimeSeries_Example1_Template_0.3.1-alpha_generated.yaml
  $ python yodatool.py loaddatabase --type timeseries --engine postgresql --dbname odm2 --address localhost:5432 --username odm2 --password odm2 --scriptfilename yodatool/blank_schema_scripts/ODM2_for_PostgreSQL.sql yodatool/examples/generatedYODAfiles/YODA_TimeSeries_Example1_Template_0.3.1-alpha_generated.yaml
```
Intitial thoguhts:
  * yoda validate [format] [file] [strict?]
     * validates a yoda file. formats [TS-timeseries, SP-Specimens]
     * [strict] true(default). follow vocabs. false = allow loose
  * yoda loaddatabase [connection] [options] [strict?]
     * loads data to a specified database connection
     * [strict] true(default). follow vocabs. false = ADD terms
  * yoda load [yodafile] [url] [--validate=true]
     * load yoda file to a specified ODM2 Webservice
     * option to turn off validate
  * yoda get [datasetid] [url] [--format]
     *  get dataset from a ODM2 webservice in a specified format
  * yoda generate [input xlsx file] [output file]
     * generate and validate a yoda from specified XLSX file, save to file
  * yoda
     * opens a gui
  * yoda help
  * yoda cvsubmit [format] [file]
    * submit unknown controlled terms to cv service

### Credits

This work was supported by National Science Foundation Grants [EAR-1224638](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1224638) and [ACI-1339834](http://www.nsf.gov/awardsearch/showAward?AWD_ID=1339834). Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
