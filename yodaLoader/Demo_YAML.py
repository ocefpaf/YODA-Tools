import sys
import os

import pprint

pp = pprint.PrettyPrinter(indent=8)





try:
    # check to make sure that these imports happen
    from odm2api.ODM2.models import *
    # from ODM2PythonAPI.src.api.ODM2.new_services import createService
    from odm2api.ODMconnection import dbconnection
    from YAML.yamlFunctions import YamlFunctions
except ImportError as e:
    print(e)
    sys.exit(0)





# Create a connection to the ODM2 database


# session_factory = dbconnection.createConnection('mysql', 'jws.uwrl.usu.edu', 'odm2', 'ODM', 'ODM123!!')

# session_factory = dbconnection.createConnection('mssql', 'arroyoodm2', 'LBRODM2', 'ODM', 'odm')
# session_factory = dbconnection.createConnection('postgresql', 'localhost', 'ODM2', 'odm', 'odm')
session_factory = dbconnection.createConnection('mysql', "localhost", 'ODM2', 'ODM', 'odm')

# session_factory = dbconnection.createConnection('mysql', 'arroyo.uwrl.usu.edu', 'LBRODM2', 'Stephanie', 'odm')
# session_factory = dbconnection.createConnection('sqlite', '/Users/stephanie/DEV/DBs/ODM2.sqlite', 2.0)


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

files.append(os.path.join('.', 'test.yaml'))





import timeit

start = timeit.default_timer()
yaml_load = YamlFunctions(_session, _engine)

yaml_load.loadFromFile(files[0])
# yaml_load.saveToDB()

print()
print("-------- Performance Results using python module: timeit --------")
print("Loaded YAML file in ", timeit.default_timer() - start, " seconds")

# yaml_load._session.autoflush = False

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

# pp.pprint("---Example YAML reading <MeasResults>---")
# pp.pprint(measurement_results)
# print()
# pp.pprint("--Example YAML reading <MeasResultValues>--")
# pp.pprint(meas_result_values)
# print()
#

yaml_load.saveToDB()



