
import datetime
import copy
import yaml

class YamlPrinter():

    _references= {}
    def get_header(self):
        yoda_header = "---\n"
        yoda_header += "YODA:\n"

        yoda_header += " - {"
        yoda_header += "Version: \"{0}\", ".format("0.1.0")
        yoda_header += "Profile: \"{0}\", ".format("SpecimenTimeSeries")
        yoda_header += "CreationTool: \"{0}\", ".format("YodaConverter")
        yoda_header += "DateCreated: \"{0}\", ".format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
        yoda_header += "DateUpdated: \"{0}\"".format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))
        yoda_header += "}\n"
        return yoda_header.replace('None', 'NULL')

    def handle_inheritance(self, apiobjs):
        # break into groups of object types (specimen vs site)
        from collections import defaultdict
        objlist = defaultdict(list)
        text = ""

        for obj in apiobjs:
            objlist[obj.__class__.__name__].append(obj)

        index = 0
        # call current function with each list, send in class name
        for k, v in objlist.items():
            text += self.print_objects(objlist[k],  index)
            index += len(objlist[k])
        return text

    def print_objects(self, apiobjs, ind = 0 ):
        # TODO handle inheritance objects
        objname = apiobjs[0].__class__.__name__

        text = objname + ":\n"

        index = 1 + ind
        for obj in apiobjs:

            primarykey = obj.__mapper__.primary_key[0].name
            valuedict = obj.__dict__.copy()

            #find the attribute name of the primary key
            for v in valuedict:
                if v.lower() == obj.__mapper__.primary_key[0].name:
                    # pop unwanted items from the dictionary
                    valuedict.pop(v)
                    if v != "BridgeID":
                        primarykey = v
                    else:
                        #what to do if the primary key is BridgeID?
                        if objname[-1] == "s":
                            primarykey = objname[:-1] + "ID"
                        else:
                            primarykey = objname + "ID"
                    break

            #remove all id's from the dictionary
            for k in valuedict.keys():
                if "id" in k.lower():
                    del valuedict[k]

            #assign the reference value for objects
            for key in dir(obj):
                if "obj" in key.lower():  # key.contains("Obj"):
                    try:
                        att = getattr(obj, key)
                        valuedict[key] = self._references[getattr(obj, key)]
                        #todo: featureaction, samplingfeatureobj not being found
                    except Exception as e:
                        print ("cannot find {} in {}. Error:{} in YamlPrinter".format(key, obj.__class__.__name__, e))

            self._references[obj] = '*{}{:0>4d}'.format(primarykey, index)
            text += ' - &{}{:0>4d} '.format(primarykey, index)
            text += self.print_dictionary(valuedict)
            index += 1
        return text

    def print_dictionary(self, dict):
        from numbers import Number
        final_string= "{"
        for k, v in dict.items():
            #if the item is null don't print it
            if isinstance(v, Number):
                final_string += '{}: {}, '.format(k, v)
            if isinstance(v, basestring):
                if '*' in v:
                    final_string += '{}: {}, '.format(k, v)
                else:
                    final_string += '{}: "{}", '.format(k, v)
            if isinstance(v, datetime.datetime):
                final_string += '{}: "{}", '.format(k, v.strftime("%Y-%m-%d %H:%M"))

        final_string = "{}}}\n".format(final_string[:-2])

        return final_string

    def print_to_file(self, objname, file, data):

        if objname in data:
            # check to see if this is an inherited object
            if data[objname][0].__class__ != data[objname][0]._sa_instance_state.key[0]:
                file.write(self.handle_inheritance(apiobjs=data[objname]))
            else:
                file.write(self.print_objects(data[objname]))

    def generate_ts_objects(self, data):
        pass
    def print_yoda(self, out_file, data):
        with open(out_file, 'w') as yaml_schema_file:
            print data.keys()
            #header
            yaml_schema_file.write(self.get_header())
            #dataset
            self.print_to_file("datasets", yaml_schema_file, data)
            #organization
            self.print_to_file("organizations", yaml_schema_file, data)
            #people
            self.print_to_file("people", yaml_schema_file, data)
            #affiliations
            self.print_to_file("affiliations", yaml_schema_file, data)
            #citations
            self.print_to_file("citations", yaml_schema_file, data)
            #authorlists
            self.print_to_file("authorlists", yaml_schema_file, data)
            #datasetcitations
            self.print_to_file("datasetcitations", yaml_schema_file, data)
            #spatialreferences
            self.print_to_file("spatialreferences", yaml_schema_file, data)
            #samplingfeatures: Not explicitly printed, should be included in sites and specimen objects
            #sites
            # self.print_to_file("sites", yaml_schema_file, data)
            #specimens
            # self.print_to_file("specimens", yaml_schema_file, data)

            self.print_to_file("samplingfeatures", yaml_schema_file, data)
            #relatedfeatures
            self.print_to_file("relatedfeatures", yaml_schema_file, data)
            #units
            self.print_to_file("units", yaml_schema_file, data)
            #annotations
            self.print_to_file("annotations", yaml_schema_file, data)
            #methods
            self.print_to_file("methods", yaml_schema_file, data)
            #variables
            self.print_to_file("variables", yaml_schema_file, data)
            #proc level
            self.print_to_file("processinglevels", yaml_schema_file, data)
            #action
            self.print_to_file("actions", yaml_schema_file, data)
            #featureaction
            self.print_to_file("featureactions", yaml_schema_file, data)
            #actionby
            self.print_to_file("actionby", yaml_schema_file, data)
            #relatedActions
            self.print_to_file("relatedactions", yaml_schema_file, data)
            #result Not explicitly printed, should be included in measurement or timeseries results
            self.print_to_file("results", yaml_schema_file, data)
            #measurement results
            self.print_to_file("measurementresults", yaml_schema_file, data)
            #timeseriesresult
            self.print_to_file("timeseriesresults", yaml_schema_file, data)
            #datasetresults
            self.print_to_file("datasetsresults", yaml_schema_file, data)
            # measurementResultValues
            self.print_to_file("measurementresultvalues", yaml_schema_file, data)
            #timeseriesresultvalues - ColumnDefinitions:, Data:
            val = "timeseriesresultvalues"
            if val in data:
                yaml_schema_file.write(self.generate_ts_objects(data[val]))
            #MeasurementResultValueAnnotations
            self.print_to_file("measurementresultvalueannotations", yaml_schema_file, data)


            yaml_schema_file.write("...")

