import sys
import os

import pprint

pp = pprint.PrettyPrinter(indent=8)

# this_file = os.path.realpath(__file__)
# print("This file: ", this_file)
# directory = os.path.dirname(this_file)
# print("Directory: ", directory, os.listdir(directory))
# #api_directory = os.path.join(directory, 'ODM2PythonAPI', 'YAML', 'api')
# src_directory = os.path.join(directory, 'YAML')
#
# #print("API_PATH: ", api_directory)
# print("SRC_PATH: ", src_directory)
#
#
# #if not api_directory in sys.path:
# #    sys.path.append(api_directory)
# if not src_directory in sys.path:
#     sys.path.append(src_directory)
#
# # pp.pprint(sys.path)
#
# try:
#     # check to make sure that these imports happen
#     from src.api.ODM2.models import *
#     # from ODM2PythonAPI.src.api.ODM2.new_services import createService
#     from src.api.ODMconnection import dbconnection
#     from YAML.yamlFunctions import YamlFunctions
# except ImportError as e:
#     print(e)
#     sys.exit(0)


from api.ODM2.models import *
from api.ODMconnection import dbconnection
from YAML.yamlFunctions import YamlFunctions

# Create a connection to the ODM2 database


#session_factory = dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm2', 'ODM', 'ODM123!!')

# session_factory = dbconnection.createConnection('mssql', '(local)', 'ODM2SS', 'ODM', 'odm')
# conn = dbconnection.createConnection('postgresql', 'localhost', 'ODMSS', 'Stephanie', 'odm')
# session_factory = dbconnection.createConnection('mysql', "localhost", 'ODM2', 'ODM', 'odm')

session_factory = dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'ODM2', 'ODM', 'ODM123!!')
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
# files.append(os.path.join('.', 'YODA-File', 'ExcelTemplates', 'Prototypes', 'Timeseries_Template_Working_modified.yaml'))
files.append(os.path.join('.', 'test.yaml'))
# files.append('/Users/stephanie/Documents/YODA_Specimen_TEMPLATE_NOERRORS.xlsm')
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
persons = _session.query(People).limit(50).all()
datasets = _session.query(DataSets).limit(50).all()
citations = _session.query(Citations).limit(50).all()
authorlists = _session.query(AuthorLists).limit(50).all()
spatial_references = _session.query(SpatialReferences).limit(50).all()

sampling_features = _session.query(SamplingFeatures).limit(50).all()
sites = _session.query(Sites).limit(50).all()

methods = _session.query(Methods).limit(50).all()
variables = _session.query(Variables).limit(50).all()
units = _session.query(Units).limit(50).all()
processing_levels = _session.query(ProcessingLevels).limit(50).all()
actions = _session.query(Actions).limit(50).all()
results = _session.query(Results).limit(50).all()
# noinspection PyUnboundLocalVariable
time_series_results = _session.query(TimeSeriesResults).limit(50).all()
time_series_result_values = _session.query(TimeSeriesResultValues).limit(50).all()
# yaml_load._session.commit()

measurement_results = _session.query(MeasurementResults).all()
meas_result_values = _session.query(MeasurementResultValues).limit(50).all()

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

pp.pprint("--Example YAML reading <TimeSeriesResultValues>--")
pp.pprint(time_series_result_values)
print()

pp.pprint("---Example YAML reading <MeasResults>---")
pp.pprint(measurement_results)
print()
pp.pprint("--Example YAML reading <MeasResultValues>--")
pp.pprint(meas_result_values)
print()





