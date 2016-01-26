__author__ = 'Choonhan Youn'

import argparse
import copy
import inspect
import logging

import yaml

from load.YODAloader import yodaLoad
from validate.cvvalidator import CVvalidator
from validate.timeseriesvalidator import TSvalidator

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

def yoda_validate(args):
    print "Type: %s Level: %s CV type: %s" % (args.type,args.level,args.cvtype)
    if args.level in [1,2,3]:
        if args.type == 'timeseries':
            validate_timeseries(args.yoda_file,args.level,args.cvtype)
        else:
            print "usage: data type: measurement, timeseries"
    else:
        print "usage: validation level: 1 for coarse, 2 for medium, 3 for fine"

def yoda_load(args):
    #print "Type: %s Level: %s" % (args.type,args.level)
    if args.type == 'timeseries':
        load_timeseries(args)

def validate_timeseries(yodaFile, level=1,cvtype=False):

    #logger = yoda_logger(logging.INFO,logging.WARNING)
    logger = yoda_logger(logging.INFO)
    stream = file(yodaFile)
    yaml_data = yaml.load(stream)

    if 'YODA' in yaml_data:
        yaml_data.pop('YODA')

    yaml_data_cv = copy.copy(yaml_data)
    tsvalidator = TSvalidator(logger)
    flag = tsvalidator.validate(level,yaml_data)

    #Validate cv types
    if cvtype:
        cvval = CVvalidator(logger)
        flag = cvval.validate(yaml_data_cv)

    print "Validation Result: %s" % flag
    if not flag:
        print "please look into the generated log file."
    return flag

def load_timeseries(args):
    logger = yoda_logger(logging.INFO,logging.WARNING)
    stream = file(args.yoda_file)
    yaml_data = yaml.load (stream)

    yodadb = yodaLoad()
    yodadb.db_info()

    yodadb.data_load(yaml_data)


def main():
    parser = argparse.ArgumentParser()

    default_parser = argparse.ArgumentParser(add_help=False)
    default_parser.add_argument('yoda_file', type=str, help='yoda file name')

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_validate = subparsers.add_parser('validate', parents=[default_parser])
    parser_validate.add_argument('--type', type=str, default="timeseries", required=False, help='data type: measurement, timeseries')
    parser_validate.add_argument('--level', type=int, default=1, required=False, help='validation level: 1 for coarse, 2 for medium, 3 for fine')
    parser_validate.add_argument('-c','--cvtype', action='store_true', help='validate CV types')
    parser_validate.set_defaults(func=yoda_validate)

    parser_load = subparsers.add_parser('load', parents=[default_parser])
    parser_load.add_argument('--type', type=str, default="timeseries", required=False, help='data type: measurement, timeseries')
    parser_load.set_defaults(func=yoda_load)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
