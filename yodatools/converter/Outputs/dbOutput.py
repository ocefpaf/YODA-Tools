from yodatools.converter.Abstract import iOutputs
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services import *
from odm2api.ODM2.models import setSchema, Sites, Results, SamplingFeatures, Specimens, MeasurementResults, TimeSeriesResults
import logging
import sqlite3

class dbOutput(iOutputs):

    def __init__(self, file_path=None, connection_string = None):
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
        self.connect_to_db(connection_string)
        
        #datasets
        self.check("datasets", self.data)
        # organization
        self.check("organizations", self.data)
        # people
        self.check("people", self.data)
        # affiliations
        self.check("affiliations", self.data)
        # citations
        self.check("citations", self.data)
        # authorlists
        self.check("authorlists", self.data)
        # datasetcitations
        self.check("datasetcitations", self.data)
        # spatialreferences
        self.check("spatialreferences", self.data)
        # samplingfeatures: 
        self.check("samplingfeatures", self.data)
        # relatedfeatures
        self.check("relatedfeatures", self.data)
        # units
        self.check("units", self.data)
        # annotations
        self.check("annotations", self.data)
        # methods
        self.check("methods", self.data)
        # variables
        self.check("variables", self.data)
        # proc level
        self.check("processinglevels", self.data)
        # action
        self.check("actions", self.data)
        # featureaction
        self.check("featureactions", self.data)
        # actionby
        self.check("actionby", self.data)
        # relatedActions
        self.check("relatedactions", self.data)
        # result
        self.check("results", self.data)
        # datasetresults
        self.check("datasetsresults", self.data)
        # measurementResultValues
        self.check("measurementresultvalues", self.data)
        # MeasurementResultValueAnnotations
        self.check("measurementresultvalueannotations", self.data)
        # timeseriesresultvalues - ColumnDefinitions:, data:
        val = "timeseriesresultvalues"
        if val in self.data:
            self.save_ts(self.data[val])

        self._session_out.commit()

    def save_ts(self, values):
        pass

    def check(self, objname, data):

        if objname in data:
            vals = self.add_to_db( data[objname])
            self.added_objs[objname] =vals

    def add_to_db(self,  values):
        added = []
        from odm2api.ODM2.models import _changeSchema
        _changeSchema(None)
        for obj in values:
            try:
                valuedict = obj.__dict__.copy()
                valuedict = self.get_new_objects(obj, valuedict)
                valuedict.pop("_sa_instance_state")

                #delete primary key
                for v in valuedict.keys():
                    if v.lower() == obj.__mapper__.primary_key[0].name:
                        del valuedict[v]
                    elif "obj" in v.lower():
                        del valuedict[v]
                setSchema(self._engine_out)
                model = self.check_model(attr=obj)
                added.append(self.get_or_create(self._session_out, model, **valuedict))

            except Exception as e:
                print e
                self._session_out.rollback()
                # raise e
        return added

    def check_model(self, attr):
        model = type(attr)
        # if isinstance(attr, Sites) or isinstance(attr, Specimens):
        #     model = SamplingFeatures
        # elif isinstance(attr, MeasurementResults) or isinstance(attr, TimeSeriesResults):
        #     return Results

        return model

    def get_new_objects(self, obj, valuedict):
        for key in dir(obj):
            if "obj" in key.lower():  # key.contains("Obj"):
                try:
                    att = getattr(obj, key)
                    if att is not None:
                        attdict = att.__dict__.copy()
                        # for v in attdict.keys():
                        #     if "id" in v.lower() and "uuid" not in v.lower():
                        #         del attdict[v]
                        pk = None
                        for k in attdict.keys():
                            if k.lower() == att.__mapper__.primary_key[0].name:
                                pk = k
                                del attdict[k]
                            elif "obj" in k.lower():
                                del attdict[k]
                        attdict.pop("_sa_instance_state")
                        attdict = self.get_new_objects(att, attdict)

                        model = self.check_model(attr =att)
                        setSchema(self._engine_out)

                        get = getattr(model, pk)

                        # new_obj = self._session_out.query(model).filter_by(**attdict).first()
                        new_obj = self.get_inherited(self._session_out, model, **attdict)
                        # for s in self.added_objs["samplingfeatures"]:
                        #     if s == att:
                        #         new_obj = s

                        objkey = key.replace("Obj", "ID")
                        newkey = objkey
                        if objkey == "RelatedFeatureID":
                            newkey = "SamplingFeatureID"
                        elif objkey == "RelatedActionID":
                            newkey = "ActionID"
                        valuedict[objkey] = getattr(new_obj, newkey)

                except Exception as e:
                    print ("cannot find {} in {}. Error:{} in dbOutput".format(key, obj.__class__.__name__, e))
        return valuedict


    def get_inherited(self, sess, model, **kwargs):
        uuid = {}
        for key in kwargs.keys():
            if "uuid" in key.lower():
                uuid[key] = kwargs[key]
                break
        try:
            if len(uuid) > 0:
                instance = sess.query(model).filter_by(**uuid).first()
            else:
                instance = sess.query(model).filter_by(**kwargs).first()
            return instance
        except:
            return None

    def get_or_create(self, sess, model, **kwargs):
        # instance = sess.query(model).filter_by(**kwargs).first()
        instance = self.get_inherited(sess, model, **kwargs)

        if instance:
            return instance
        else:
            instance = model(**kwargs)
            # print instance
            new_instance = sess.merge(instance)
            sess.flush()
            return new_instance

