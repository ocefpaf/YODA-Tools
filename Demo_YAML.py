import sys
import os

import pprint

pp = pprint.PrettyPrinter(indent=8)

this_file = os.path.realpath(__file__)
print("This file: ", this_file)
directory = os.path.dirname(this_file)
print("Directory: ", directory, os.listdir(directory))
api_directory = os.path.join(directory, 'ODM2PythonAPI', 'src', 'api')
src_directory = os.path.join(directory, 'src')

print("API_PATH: ", api_directory)
print("SRC_PATH: ", src_directory)


if not api_directory in sys.path:
    sys.path.append(api_directory)
if not src_directory in sys.path:
    sys.path.append(src_directory)

pp.pprint(sys.path)

try:
    # check to make sure that these imports happen
    from ODM2.models import *
    # from ODM2PythonAPI.src.api.ODM2.new_services import createService
    from ODMconnection import dbconnection
    from YAML.yamlFunctions import YamlFunctions
except ImportError as e:
    print(e)
    sys.exit(0)




# Create a connection to the ODM2 database
# ----------------------------------------
# conn = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'ODM123!!')

session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'root', 'zxc')
# session_factory = dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm2', 'ODM', 'ODM123!!')

# session_factory = dbconnection.createConnection('mssql', '(local)', 'ODM2SS', 'ODM', 'odm')
# conn = dbconnection.createConnection('postgresql', 'arroyo.uwrl.usu.edu:5432', 'ODMSS', 'Stephanie', 'odm')
# conn = dbconnection.createConnection('mysql', '127.0.0.1:3306', 'ODM2', 'Stephanie', 'odm')

# Create a connection for each of the schemas. Currently the schemas each have a different
# connection but it will be changed to all the services sharing a connection
# ----------------------------------------------------------------------------------------

_session = session_factory.getSession()
_engine = session_factory.engine

# Demonstrate loading a yaml file into an ODM2 database

# Demonstrate loading a yaml file into an ODM2 database
print()
print("---------------------------------------------------------------------")
print("---------                                                  ----------")
print("-------- \tExample of Loading yaml file into SQLAlchemy \t---------")
print("---------                                                  ----------")
print("---------------------------------------------------------------------")

files = []
# files.append(os.path.join('.', 'ODM2/YAML/iUTAH_MultiTimeSeriesExample_CompactHeader2.yaml'))
# files.append(os.path.join('.', 'ODM2/YAML/Examples/iUTAH_SpecimenTimeSeriesExample_CompactHeader.yaml'))
# files.append(os.path.join('.', 'ODM2/YAML/iUTAH_MultiTimeSeriesExample_CompactHeader.yaml'))
# files.append(os.path.join('.', 'ODM2/YAML/Examples/iUTAH_MultiTimeSeriesExample_LongHeader+AKA.yaml'))
# files.append(os.path.join('.', 'ODM2/YAML/Examples/iUTAH_MultiTimeSeriesExample_LongHeader.yaml'))
# files.append(os.path.join('.', 'ODM2/YAML/Examples/test.yaml'))
# files.append(os.path.join('.', 'YODA-File', 'ExcelTemplates', 'Prototypes', 'Timeseries_Template_Working.yaml'))
files.append(os.path.join('.', 'YODA-File', 'ExcelTemplates', 'Prototypes', 'Timeseries_Template_Working_modified.yaml'))

## Working files
# files.append(os.path.join('.', 'ODM2/YAML/Examples/iUTAH_MultiTimeSeriesExample_CompactHeader.yaml'))

_session.autoflush = False

import timeit

start = timeit.default_timer()
yaml_load = YamlFunctions(_session, _engine)

yaml_load.loadFromFile(files[0])

print()
print("-------- Performance Results using python module: timeit --------")
print("Loaded YAML file in ", timeit.default_timer() - start, " seconds")

# yaml_load._session.autoflush = False
_session.flush()
persons = _session.query(People).all()
datasets = _session.query(Datasets).all()
citations = _session.query(Citations).all()
authorlists = _session.query(AuthorLists).all()
spatial_references = _session.query(SpatialReferences).all()

sampling_features = _session.query(SamplingFeatures).all()
sites = _session.query(Sites).all()

methods = _session.query(Methods).all()
variables = _session.query(Variables).all()
units = _session.query(Units).all()
processing_levels = _session.query(ProcessingLevels).all()
actions = _session.query(Actions).all()
results = _session.query(Results).all()
# noinspection PyUnboundLocalVariable
time_series_results = _session.query(TimeSeriesResults).all()

# yaml_load._session.commit()

print()
pp.pprint("---Example YAML reading <People>---")
pp.pprint(persons)
print()
pp.pprint("---Example YAML reading <Citation>---")
pp.pprint(citations)
print()
pp.pprint("---Example YAML reading <AuthorLists>---")
pp.pprint(authorlists)
print()
pp.pprint("---Example YAML reading <DataSets>---")
pp.pprint(datasets)
print()
pp.pprint("---Example YAML reading <Spatial References>---")
pp.pprint(spatial_references)
print()
pp.pprint("---Example YAML reading <Methods>---")
pp.pprint(methods)
print()
pp.pprint("---Example YAML reading <Variables>---")
pp.pprint(variables)
print()
pp.pprint("---Example YAML reading <Units>---")
pp.pprint(units)
print()
pp.pprint("---Example YAML reading <ProcessingLevels>---")
pp.pprint(processing_levels)
print()
pp.pprint("---Example YAML reading <Sites>---")
pp.pprint(sites)
print()
pp.pprint("---Example YAML reading <SamplingFeatures>---")
pp.pprint(sampling_features)
print()
pp.pprint("---Example YAML reading <Actions>---")
pp.pprint(actions)
print()

pp.pprint("---Example YAML reading <Results>---")
pp.pprint(results)
print()

pp.pprint("---Example YAML reading <TimeSeriesResults>---")
pp.pprint(time_series_results)
print






