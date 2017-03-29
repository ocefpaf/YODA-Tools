__author__ = 'Choonhan Youn'

import argparse
import copy
import inspect
import logging
import os.path
import sys

import yaml

from yodatools.excelparser.generate.measurement.measurement_yoda import MeasurementYoda
# from yodatools.generate.timeseries.v0_3_1.timeseries_yoda import TimeseriesYoda
from yodatools.excelparser.generate.timeseries.v0_3_2.timeseries_yoda import TimeseriesYoda
from yodatools.excelparser.load.YODAloader import yodaLoad
from yodatools.excelparser.validate.cvvalidator import CVvalidator
from yodatools.excelparser.validate.timeseriesvalidator import TSvalidator


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
        elif args.type == 'measurement':
            print 'The measurement type is not implemnted yet.'
            print "usage: data type: measurement, timeseries"
        else:
            print "usage: data type: measurement, timeseries"
    else:
        print "usage: validation level: 1 for coarse, 2 for medium, 3 for fine"

def yoda_load(args):
    print "Type: %s" % args.type
    print "DB engine: %s" % args.engine
    print "DB name: %s" % args.dbname
    print "DB server address: %s" % args.address
    print "DB username: %s" % args.username
    print "DB password: %s" % args.password
    print "DB blank schema file: %s" % args.scriptfilename
    if not os.path.exists(args.scriptfilename):
        print "The schema script file, \"%s\", is not existed!!!" % args.scriptfilename
        sys.exit(0)
    if args.type == 'timeseries':
        load_timeseries(args)
    elif args.type == 'measurement':
        print 'The measurement type is not implemnted yet.'
        print "usage: data type: measurement, timeseries"
    else:
        print "usage: data type: measurement, timeseries"

def yoda_generate(args):
    print "Type: %s" % args.type
    if args.type == 'measurement':
        generate_measurement(args)
    elif args.type == 'timeseries':
        generate_timeseries(args)
    else:
        print "usage: data type: measurement, timeseries"

def validate_timeseries(yodaFile, level=1,cvtype=False):

    #logger = yoda_logger(logging.INFO,logging.WARNING)
    logger = yoda_logger(logging.INFO)
    logger.info("Validating YODA file: {0}".format(yodaFile))
    stream = file(yodaFile)
    yaml_data = yaml.load(stream)

    if 'YODA' in yaml_data:
        yaml_data.pop('YODA')

    yaml_data_cv = copy.copy(yaml_data)
    tsvalidator = TSvalidator(logger)
    flag = tsvalidator.validate(level,yaml_data)
    print "Validation Result: %s" % flag
    if not flag:
        print "please look into the generated log file."

    #Validate cv types
    cv_flag = True
    if cvtype:
        logger.info("Validating CV")
        cvval = CVvalidator(logger)
        cv_flag = cvval.validate(yaml_data_cv)

        print "CV validation Result: %s" % cv_flag
        if not cv_flag:
            print "please look into the generated log file."

    if flag and cv_flag:
        return True
    else:
        return False

def load_timeseries(args):
    logger = yoda_logger(logging.INFO,logging.WARNING)
    stream = file(args.yoda_file)
    yaml_data = yaml.load(stream)

    yodadb = yodaLoad()
    yodadb.db_setup(args.engine,args.dbname,
                    args.address,args.username,args.password,
                    args.scriptfilename)
    yodadb.data_load(yaml_data)

def generate_measurement(args):
    yoda_format = MeasurementYoda(args.xl_file)
    yoda_format.create_yoda(args.out_file)

def generate_timeseries(args):
    yoda_format = TimeseriesYoda(args.xl_file)
    yoda_format.create_yoda(args.out_file)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    # A validation command
    validate_parser = subparsers.add_parser('validate', help='Validate yoda file')
    validate_parser.add_argument('yoda_file', type=str, help='yoda file name')
    validate_parser.add_argument('--type', type=str, default="timeseries", required=False, help='data type: measurement, timeseries')
    validate_parser.add_argument('--level', type=int, default=1, required=False, help='validation level: 1 for coarse, 2 for medium, 3 for fine')
    validate_parser.add_argument('-c','--cvtype', action='store_true', help='validate CV types')
    validate_parser.set_defaults(func=yoda_validate)

    # A generate command
    generate_parser = subparsers.add_parser('generate', help='Generate YODA file')
    generate_parser.add_argument('xl_file', type=str, action='store', help='xl file name (input)')
    generate_parser.add_argument('out_file', type=str, action='store', help='yaml file name (output)')
    generate_parser.add_argument('--type', type=str, default="measurement", required=False, help='data type: measurement, timeseries')
    generate_parser.set_defaults(func=yoda_generate)

    # A loaddatabase command
    load_parser = subparsers.add_parser('loaddatabase', help='Load yoda file into database')
    load_parser.add_argument('yoda_file', type=str, help='yoda file name')
    load_parser.add_argument('--type', type=str, default="timeseries", required=False, help='data type: measurement, timeseries')
    load_parser.add_argument('--engine', type=str, default="sqlite", required=False, help='ODM2 database engine (sqlite,postgresql)')
    load_parser.add_argument('--dbname', type=str, default="odm2", required=False, help='ODM2 database name')
    load_parser.add_argument('--address', type=str, default="localhost", required=False, help='ODM2 server address(host:port)')
    load_parser.add_argument('--username', type=str, default="odm2", required=False, help='ODM2 database user name')
    load_parser.add_argument('--password', type=str, default="odm2", required=False, help='ODM2 database password')
    load_parser.add_argument('--scriptfilename', type=str, default="ODM2_for_SQLite.sql", required=False, help='ODM2 blank schema script')

    load_parser.set_defaults(func=yoda_load)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()