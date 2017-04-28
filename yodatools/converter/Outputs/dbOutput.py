from yodatools.converter.Abstract import iOutputs
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services import *
import logging
import sqlite3

class dbOutput(iOutputs):

    def __init__(self, file_path, connection_string = None):
        if connection_string:
            self.connect_to_db(connection_string)

    def connect_to_db(self, connection_string):
        self.session_factory_out = dbconnection.createConnectionFromString(connection_string)
        self._session_out = self.session_factory_out.getSession()
        self._engine = self.session_factory_out.engine
        return self._session_out

    def save(self, session, connection_string):
        data = self.parseObjects(session)
        session_out = self.connect_to_db(connection_string)

        # for key in data:
        #     self.check(session_out, data[key])
        self.check("datasets", data, session_out)
        # organization
        self.check("organizations", data, session_out)
        # people
        self.check("people", data, session_out)
        # affiliations
        self.check("affiliations", data, session_out)
        # citations
        self.check("citations", data, session_out)
        # authorlists
        self.check("authorlists", data, session_out)
        # datasetcitations
        self.check("datasetcitations", data, session_out)
        # spatialreferences
        self.check("spatialreferences", data, session_out)
        # samplingfeatures: Not explicitly printed, should be included in sites and specimen objects
        # sites
        # self.check("sites", data, session_out)
        # specimens
        # self.check("specimens", data, session_out)

        self.check("samplingfeatures", data, session_out)
        # relatedfeatures
        self.check("relatedfeatures", data, session_out)
        # units
        self.check("units", data, session_out)
        # annotations
        self.check("annotations", data, session_out)
        # methods
        self.check("methods", data, session_out)
        # variables
        self.check("variables", data, session_out)
        # proc level
        self.check("processinglevels", data, session_out)
        # action
        self.check("actions", data, session_out)
        # featureaction
        self.check("featureactions", data, session_out)
        # actionby
        self.check("actionby", data, session_out)
        # relatedActions
        self.check("relatedactions", data, session_out)
        # result Not explicitly printed, should be included in measurement or timeseries results
        self.check("results", data, session_out)
        # #measurement results
        # self.check("measurementresults", data, session_out)
        # #timeseriesresult
        # self.check("timeseriesresults", data, session_out)
        # datasetresults
        self.check("datasetsresults", data, session_out)
        # measurementResultValues
        self.check("measurementresultvalues", data, session_out)
        # timeseriesresultvalues - ColumnDefinitions:, Data:
        val = "timeseriesresultvalues"
        if val in data:
            self.save_ts(data[val], session_out)
        # MeasurementResultValueAnnotations
        self.check("measurementresultvalueannotations", data, session_out)

        session_out.commit()

    def save_ts(self, values, session_out,):
        pass

    def check(self, objname, data, session_out ):
        if objname in data:
            self.add_to_db(session_out,  data[objname])

    def add_to_db(self, session_out,  values):
        try:
            for obj in values:
                valuedict = obj.__dict__
                try:
                    valuedict.pop("_sa_instance_state")
                    for v in valuedict:
                        if v.lower() == obj.__mapper__.primary_key[0].name:
                            primarykey = v
                            break
                    # pop primary key
                    valuedict.pop(primarykey)
                except Exception as e:
                    print e

                return self.get_or_create(session_out, type(obj), **valuedict)
                # session_out.add(obj)

        except Exception as e:
            print e
            # raise e



    def get_or_create(self, sess, model, **kwargs):
        instance = sess.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            sess.merge(instance)
            sess.flush()
            return instance

