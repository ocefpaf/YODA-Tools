# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Stephanie'


from argparse import ArgumentParser
import logging

import time



'''
this file is going to contain all of the logic for running the conversion from inputtype to output type
it will all so contain all of the command line functionality
the ui will import this file and call the main function

'''

def main():
    pass


#command line stuff
# Application entry point.
if __name__ == "__main__":
    parser = ArgumentParser(description="YodaTools")

    parser.add_argument('-i', '--input', dest="inputFile",\
        help="Specify a yodaparser configuration file in the form of one of these formats:\n1. A single yodaparser (.yaml) file.\n"
             "2. An Excel YODA template.\n", required=True, action="store")
    # parser.add_argument('-e', '--excel', dest="excelFile",\
    #     help="Specify a single excel path to save the converted data too.", required=False, action="store")
    parser.add_argument('-y', '--yoda', dest="yodaFile",\
        help="Specify a single yoda file path to save the converted data too.", required=False, action="store")
    # parser.add_argument('-d', '--database', dest="dbconn",\
    #                      help="Specify a Database connection. " \
    #                           "Format: {engine}+{driver}://{user}:{pass}@{address}/{db}\n"" \
    #                           ""mysql+pymysql://ODM:odm@localhost/odm2\n"" \
    #                           ""mssql+pyodbc://ODM:123@localhost/odm2\n"" \
    #                           ""postgresql+psycopg2://ODM:odm@test.uwrl.usu.edu/odm2\n"" \
    #                           ""sqlite+pysqlite:///path/to/file",
    #                     required=False, action="store")
    args = parser.parse_args()

    start_time = time.time()
    main(args)

    # logger = logging.getLogger('YODA_logger')
    # logger.info("Running time: %s seconds" % (time.time() - start_time))