__author__ = 'Choonhan Youn'

import os
import argparse
import string
import logging
import inspect
from timeseries_dao import TimeseriesXlDao
import yaml
import json
import timeseries_models as model

from copy import deepcopy
from yaml import SafeDumper
import datetime
import odm2api.ODM2.models as odm2model
import copy

from timeseries_yoda import TimeseriesYoda

def yoda_logger(file_log_level, console_log_level = None):
    f_name = inspect.stack()[1][3] #getting function name called
    logger = logging.getLogger(f_name)
    logger.setLevel(logging.DEBUG)

    if console_log_level != None:
        console = logging.StreamHandler()
        console.setLevel(console_log_level)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)

    filehandler = logging.FileHandler("{0}.log".format(f_name))
    filehandler.setLevel(file_log_level)
    fh_format = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    filehandler.setFormatter(fh_format)
    logger.addHandler(filehandler)

    return logger

def yaml_generate(args):
    #logger = yoda_logger(logging.INFO)
    yoda_format = TimeseriesYoda(args.xl_file)
    yoda_format.create_yoda(args.out_file)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')
    parser_generate = subparsers.add_parser('generate', help='Generate YODA file')
    parser_generate.add_argument('xl_file', type=str, action='store', help='xl file name (input)')
    parser_generate.add_argument('out_file', type=str, action='store', help='yaml file name (output)')
    parser_generate.set_defaults(func=yaml_generate)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
