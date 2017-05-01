from yodatools.converter.Abstract import iOutputs
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services import *
from odm2api.ODM2.models import setSchema
import logging
import sqlite3

class dbOutput(iOutputs):

    def __init__(self, file_path, connection_string = None):
        if connection_string:
            self.connect_to_db(connection_string)
        self.added_objs= {}

    def connect_to_db(self, connection_string):
        self.session_factory_out = dbconnection.createConnectionFromString(connection_string)
        self._session_out = self.session_factory_out.getSession()
        self._engine_out = self.session_factory_out.engine
        setSchema(self._engine_out)
        return self._session_out

    def save(self, session, connection_string):
        self.data = self.parseObjects(session)
        session_out = self.connect_to_db(connection_string)
        
        #datasets
        self.check("datasets", self.data, session_out)
        # organization
        self.check("organizations", self.data, session_out)
        # people
        self.check("people", self.data, session_out)
        # affiliations
        self.check("affiliations", self.data, session_out)
        # citations
        self.check("citations", self.data, session_out)
        # authorlists
        self.check("authorlists", self.data, session_out)
        # datasetcitations
        self.check("datasetcitations", self.data, session_out)
        # spatialreferences
        self.check("spatialreferences", self.data, session_out)
        # samplingfeatures: 
        self.check("samplingfeatures", self.data, session_out)
        # relatedfeatures
        self.check("relatedfeatures", self.data, session_out)
        # units
        self.check("units", self.data, session_out)
        # annotations
        self.check("annotations", self.data, session_out)
        # methods
        self.check("methods", self.data, session_out)
        # variables
        self.check("variables", self.data, session_out)
        # proc level
        self.check("processinglevels", self.data, session_out)
        # action
        self.check("actions", self.data, session_out)
        # featureaction
        self.check("featureactions", self.data, session_out)
        # actionby
        self.check("actionby", self.data, session_out)
        # relatedActions
        self.check("relatedactions", self.data, session_out)
        # result 
        self.check("results", self.data, session_out)
        # datasetresults
        self.check("datasetsresults", self.data, session_out)
        # measurementResultValues
        self.check("measurementresultvalues", self.data, session_out)
        # MeasurementResultValueAnnotations
        self.check("measurementresultvalueannotations", self.data, session_out)
        # timeseriesresultvalues - ColumnDefinitions:, data:
        val = "timeseriesresultvalues"
        if val in self.data:
            self.save_ts(self.data[val], session_out)
        
        session_out.commit()

    def save_ts(self, values, session_out,):
        pass

    def check(self, objname, data, session_out):

        if objname in data:
            vals = self.add_to_db(session_out,  data[objname])
        self.added_objs[objname] =vals

    def add_to_db(self, session_out,  values):
        added = []
        from odm2api.ODM2.models import _changeSchema
        _changeSchema(None)
        for obj in values:
            try:
                valuedict = obj.__dict__.copy()


                # for v in valuedict:
                #     if v.lower() == obj.__mapper__.primary_key[0].name:
                #         primarykey = v
                #         break
                # # pop primary key
                # valuedict.pop(primarykey)


                for key in dir(obj):
                    if "obj" in key.lower():  # key.contains("Obj"):
                        try:

                            att = getattr(obj, key)

                            if att is not None:
                                attdict= att.__dict__.copy()
                                for v in attdict.keys():
                                #     if v.lower() == obj.__mapper__.primary_key[0].name:
                                #         del attdict[v]
                                #         break
                                    if "id" in v.lower() and "uuid" not in v.lower():
                                        del attdict[v]
                                attdict.pop("_sa_instance_state")
                                setSchema(self._engine_out)
                                new_obj = session_out.query(type(att)).filter_by(**attdict).first()
                                objkey = key.replace("Obj", "ID")
                                newkey = objkey
                                if objkey =="RelatedFeatureID":
                                    newkey = "SamplingFeatureID"
                                elif objkey == "RelatedActionID":
                                    newkey = "ActionID"

                                valuedict[objkey] = getattr(new_obj, newkey)

                        except Exception as e:
                            print ("cannot find {} in {}. Error:{} in dbOutput".format(key, obj.__class__.__name__, e))

                valuedict.pop("_sa_instance_state")

                #delete primary key
                for v in valuedict:
                    if v.lower() == obj.__mapper__.primary_key[0].name:
                        del valuedict[v]
                        break
                # for k in valuedict.keys():
                #     if "id" in k.lower() and "uuid" not in k.lower():
                #         objkey=k.replace("ID", "Obj")
                #         valuedict[k] = getattr(obj, objkey)
                #         # del valuedict[k]
                added.append(self.get_or_create(session_out, type(obj), **valuedict))
                # session_out.add(obj)

            except Exception as e:
                print e
                session_out.rollback()
                # raise e
        return added


    def get_or_create(self, sess, model, **kwargs):
        setSchema(self._engine_out)
        instance = sess.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            new_instance = sess.merge(instance)
            sess.flush()
            return new_instance

