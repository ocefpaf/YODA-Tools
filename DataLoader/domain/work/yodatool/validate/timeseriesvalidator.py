
from valideer_ts_schema import TimeseriesSchema
from valideer import ValidationError

class TSvalidator(object):

    def __init__(self,logger):
        self.logger = logger

    def validate(self,level,data):
        flag = True
        timeSeries = None
        if "TimeSeriesResultValues" in data:
            timeSeries = data.pop('TimeSeriesResultValues')

        data_columns = timeSeries['ColumnDefinitions']
        column_labels = timeSeries['Data'][0]
        del timeSeries['Data'][0]
        timeSeries = {"TimeSeriesResultValues": timeSeries}

        data_valuelist = []
        for index in range(len(data_columns)):
            column_label = "%s" % data_columns[index]['Label']
            data_label = "%s" % column_labels[index]
            #logger.info( column_label )
            #logger.info( data_label )

            if column_label != data_label:
                self.logger.error( "Both columns, (%s, %s) should be matched" % (column_label,data_label))
                raise ValidationError("Both columns, (%s, %s) should be matched" % (column_label,data_label))
            if index > 2:
                data_valuelist.append("datacolumn2")
            else:
                data_valuelist.append("datacolumn%s" % index)

        data_tuple = tuple(data_valuelist)

        S = TimeseriesSchema(self.logger)
        if level == 1:
            ts_schema = S.timeseries_schema()
            x,y = S.single_object_validate(ts_schema,data,False)
            if not y:
                self.logger.error("%s" % x)
                flag = False
        elif level == 2:
            flag = S.timeseries_object_validate(data)
        elif level == 3:
            flag = S.timeseries_detail_validate(data)

        tsv_schema = {"TimeSeriesResultValues": S.timeseriesresultvalue()}
        tsv_schema['TimeSeriesResultValues']['Data'] = [data_tuple]
        x,y = S.single_object_validate(tsv_schema,timeSeries,False)
        if not y:
            self.logger.error("%s" % x)
            flag = False

        return flag
