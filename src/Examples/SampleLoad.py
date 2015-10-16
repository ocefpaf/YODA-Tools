__author__ = 'stephanie'
import sys
import os


this_file = os.path.realpath(__file__)
print("This file: ", this_file)
directory = os.path.dirname(os.path.dirname(this_file))
print("Directory: ", directory, os.listdir(directory))

sys.path.append(directory)




try:
    # check to make sure that these imports happen
    from api.ODM2.models import *
    # from ODM2PythonAPI.src.api.ODM2.new_services import createService
    from api.ODMconnection import dbconnection
    from YAML.yamlFunctions import YamlFunctions
except ImportError as e:
    print(e)
    sys.exit(0)



# Create a connection to the ODM2 database
# ----------------------------------------
session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')


# Create a connection for each of the schemas. Currently the schemas each have a different
# connection but it will be changed to all the services sharing a connection
# ----------------------------------------------------------------------------------------



# Demonstrate loading a yaml file into an ODM2 database
print()
print("---------------------------------------------------------------------")
print("---------                                                  ----------")
print("-------- \tExample of Loading yaml file into SQLAlchemy \t---------")
print("---------                                                  ----------")
print("---------------------------------------------------------------------")

_session = session_factory.getSession()
_engine = session_factory.engine


## Working files
file='iUTAH_MultiTimeSeriesExample_CompactHeader.yaml'

_session.autoflush = False

#create a Loader
yaml_load = YamlFunctions(_session, _engine)

#Load the data into odm2 session from the yaml file
yaml_load.loadFromFile(file)
print yaml_load

#save to the database
#yaml_load.saveToDB()









