
import datetime
import copy
class YamlPrinter():


    def get_header(self):
        yoda_header = "---\n"
        yoda_header += "YODA:\n"

        yoda_header += " - {"
        yoda_header += "Version: \"{0}\", ".format("0.1.0")
        yoda_header += "Profile: \"{0}\", ".format("SpecimenTimeSeries")
        yoda_header += "CreationTool: \"{0}\", ".format("YodaConverter")
        yoda_header += "DateCreated: \"{0}\", ".format(datetime.datetime.strftime(datetime.now, '%Y-%m-%d'))
        yoda_header += "DateUpdated: \"{0}\"".format(datetime.datetime.strftime(datetime.now, '%Y-%m-%d'))
        yoda_header += "}\n"
        return yoda_header.replace('None', 'NULL')

    def print_objects(self, apiobjs):
        text = apiobjs[0].__class__.__name__+":\n"
        index = 1
        for obj in apiobjs:
            # text += '*FeatureActionID{:0>3d}'.format(index)
            key = copy.copy(obj)

            primarykey= obj.__mapper__.primary_key[0].name
            self._references[key] = '*{0}{:0>3d}'.format(primarykey, index)
            text += ' - &{0}ID{:0>3d} '.format(primarykey, index)
            valuedict = obj.__dict__.copy()
            valuedict.pop("_sa_instance_state")
            valuedict.pop(primarykey)
            text += valuedict + "\n"
            print obj


    def print_yoda(self, out_file, data):
        with open(out_file, 'w') as yaml_schema_file:

            #header
            yaml_schema_file.write(self.get_header())
            #dataset
            #organization
            #people
            #affiliations
            #citations
            #authorlists
            #datasetcitations
            #spatialreferences
            #samplingfeatures: Not explicitly printed, should be included in sites and specimen objects
            #sites
            #specimens
            #relatedfeatures
            #units
            #annotations
            #methods
            #variables
            #proc level
            #action
            #featureaction
            #actionby
            #relatedActions
            #result Not explicitly printed, should be included in measurement or timeseries results
            #measurement results
            #timeseriesresult
            #datasetresults
            #measurementResultValues
            #timeseriesresultvalues - ColumnDefinitions:, Data:

