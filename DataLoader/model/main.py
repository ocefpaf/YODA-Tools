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




#command line stuff
# Application entry point.
if __name__ == "__main__":
    parser = ArgumentParser(description="StreamingDataLoader")
    parser.add_argument('-r', '--restart',\
        action='store_true', help="Read the entire CSV file to ensure that data is correct and accounted for. This option affects performance. While the integrity of the data is checked each time the program executes, it is still recommended to use this option if you have manually modified your data file between executions.")
    parser.add_argument('-v', '--verbose',\
        action='store_true', help="Enable more verbose logging in the logfile.")
    parser.add_argument('-c', '--config', nargs='+', dest="yamlFile",\
        help="Specify a YAML configuration file in the form of one of these formats:\n1. A single YAML (.yaml) file.\n2. A list of YAML files (.yaml), deliminated by white space.\n3. A directory containing multiple YAML (.yaml) files.", required=True, action="store")
    parser.add_argument('-i', '--file', dest="csvFile",\
        help="Specify a single CSV data file to target instead of the one listed in the configuration file.", required=False, action="store")
    args = parser.parse_args()

    start_time = time.time()
    main(args)

    logger = logging.getLogger('SDL_logger')
    logger.info("Running time: %s seconds" % (time.time() - start_time))