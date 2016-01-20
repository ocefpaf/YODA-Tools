YODA-Tools
====
Prototyping a tool to validate and manage loading of YODA files

Command line:
```
yoda [command] [options]
```

```
Testing a validation for timeseries yoda file
  usage: yoda.py validate [--type TYPE] [--level LEVEL] yoda_file
  $ python src/yoda_tools/yoda.py validate --type "timeseries" --level 1 src/yoda_tools/YODA_TimeSeries_Example1_Template_0.3.0-alpha.yaml 
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
