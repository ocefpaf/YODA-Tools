__author__ = 'Choonhan Youn'

import valideer as V
import yaml
from validate.valideer_ts_schema import TimeseriesSchema, Datacolummn0, Datacolummn1, Datacolummn2, To_bool
from valideer import String, Integer, ValidationError, Validator, Datetime, Number, Date
import datetime

import os
import argparse
import string
import logging
import inspect
from urllib2 import urlopen

from YODAloader import yodaLoad

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
    print "Type: %s Level: %s" % (args.type,args.level)
    if args.type == 'timeseries':
        validate_timeseries(args.yoda_file,args.level)

def yoda_load(args):
    #print "Type: %s Level: %s" % (args.type,args.level)
    if args.type == 'timeseries':
        load_timeseries(args)

def validate_timeseries(yodaFile, level=1):

    flag = True
    #logger = yoda_logger(logging.INFO,logging.WARNING)
    logger = yoda_logger(logging.INFO)
    stream = file(yodaFile)
    yaml_data = yaml.load(stream)

    data_columns = yaml_data['TimeSeriesResultValues']['ColumnDefinitions']
    data_firstline = yaml_data['TimeSeriesResultValues']['Data'][0]

    data_valuelist = []
    for index in range(len(data_columns)):
        column_label = "%s" % data_columns[index]['Label']
        data_label = "%s" % data_firstline[index]
        #logger.info( column_label )
        #logger.info( data_label )

        if column_label != data_label:
            logger.error( "Both columns, (%s, %s) should be matched" % (column_label,data_label))
            raise ValidationError("Both columns, (%s, %s) should be matched" % (column_label,data_label))
        if index > 2:
            data_valuelist.append("datacolumn2")
        else:
            data_valuelist.append("datacolumn%s" % index)

    data_tuple = tuple(data_valuelist)
    del yaml_data['TimeSeriesResultValues']['Data'][0]

    S = TimeseriesSchema()
    if level == 1:
        ts_schema = S.timeseries_schema()
        x,y = S.single_object_validate(ts_schema,yaml_data,False)
        if not y:
            logger.error("%s" % x)
            flag = False
    elif level == 2:
        flag = S.timeseries_object_validate(logger,yaml_data)
    elif level == 3:
        flag = S.timeseries_detail_validate(logger,yaml_data)

    tsv_schema = {"TimeSeriesResultValues": S.timeseriesresultvalue()}
    tsv_schema['TimeSeriesResultValues']['Data'] = [data_tuple]
    x,y = S.single_object_validate(tsv_schema,yaml_data,False)
    if not y:
        logger.error("%s" % x)
        flag = False

    print flag
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
    parser_validate.add_argument('--type', type=str, default="timeseries", required=False, help='data type: specimen, timeseries')
    parser_validate.add_argument('--level', type=int, default=1, required=False, help='validation level: 1=coarse, 2=medium, 3=fine')
    parser_validate.set_defaults(func=yoda_validate)

    parser_load = subparsers.add_parser('load', parents=[default_parser])
    parser_load.add_argument('--type', type=str, default="timeseries", required=False, help='data type: specimen, timeseries')
    parser_load.set_defaults(func=yoda_load)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
