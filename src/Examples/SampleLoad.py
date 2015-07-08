__author__ = 'stephanie'
import sys
import os


this_file = os.path.realpath(__file__)
print("This file: ", this_file)
directory = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
print("Directory: ", directory, os.listdir(directory))

api_directory = os.path.join(directory, 'ODM2PythonAPI', 'src')
src_directory = os.path.join(directory, 'src')

print("API_PATH: ", api_directory)
print("SRC_PATH: ", src_directory)


if not api_directory in sys.path:
    sys.path.append(api_directory)
if not src_directory in sys.path:
    sys.path.append(src_directory)


# check to make sure that these imports happen
from src.api.ODM2.models import *
# from ODM2PythonAPI.src.api.ODM2.new_services import createService
from src.api.ODMconnection import dbconnection
from YAML.yamlFunctions import YamlFunctions





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









