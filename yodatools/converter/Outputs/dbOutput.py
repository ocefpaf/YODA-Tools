from odm2api.ODM2.models import _changeSchema, setSchema
# from odm2api.ODM2.services import *
from odm2api.ODMconnection import dbconnection
from yodatools.converter.Abstract import iOutputs


class dbOutput(iOutputs):

    def __init__(self, file_path=None, connection_string=None):
        if connection_string:
            self.connect_to_db(connection_string)
        self.added_objs = {}

    def connect_to_db(self, connection_string):
        self.session_factory_out = dbconnection.createConnectionFromString(connection_string)  # noqa
        self._session_out = self.session_factory_out.getSession()
        self._engine_out = self.session_factory_out.engine
        setSchema(self._engine_out)
        return self._session_out

    def save(self, session, connection_string):
        self.session_in = session
        self.data = self.parseObjects(session)
        self.connect_to_db(connection_string)

        # datasets
        self.check('datasets', self.data)
        # organization
        self.check('organizations', self.data)
        # people
        self.check('people', self.data)
        # affiliations
        self.check('affiliations', self.data)
        # citations
        self.check('citations', self.data)
        # authorlists
        self.check('authorlists', self.data)
        # datasetcitations
        self.check('datasetcitations', self.data)
        # spatialreferences
        self.check('spatialreferences', self.data)
        # samplingfeatures:
        self.check('samplingfeatures', self.data)
        # relatedfeatures
        self.check('relatedfeatures', self.data)
        # units
        self.check('units', self.data)
        # annotations
        self.check('annotations', self.data)
        # methods
        self.check('methods', self.data)
        # variables
        self.check('variables', self.data)
        # proc level
        self.check('processinglevels', self.data)
        # action
        self.check('actions', self.data)
        # featureaction
        self.check('featureactions', self.data)
        # actionby
        self.check('actionby', self.data)
        # relatedActions
        self.check('relatedactions', self.data)
        # result
        self.check('results', self.data)
        # datasetresults
        self.check('datasetsresults', self.data)
        # measurementResultValues
        self.check('measurementresultvalues', self.data)
        # MeasurementResultValueAnnotations
        self.check('measurementresultvalueannotations', self.data)
        # timeseriesresultvalues - ColumnDefinitions:, data:
        val = 'timeseriesresultvalues'
        if val in self.data:
            self.save_ts(self.data[val])

        self._session_out.commit()

    def save_ts(self, values):
        pass

    def check(self, objname, data):

        if objname in data:
            # FIXME: assinged but never used
            pass
            # vals = self.add_to_db(data[objname])
            # self.added_objs[objname] = vals

    def add_to_db(self,  values):
        # added = []

        for obj in values:
            try:
                _changeSchema(None)
                self.fill_dict(obj)
                valuedict = obj.__dict__.copy()
                valuedict = self.get_new_objects(obj, valuedict)
                valuedict.pop('_sa_instance_state')

                # Delete primary key.
                for v in valuedict.keys():
                    if v.lower() == obj.__mapper__.primary_key[0].name:
                        del valuedict[v]
                    elif 'obj' in v.lower():
                        del valuedict[v]

                model = type(obj)
                new_obj = self.get_or_create(self._session_out, model, **valuedict)  # noqa

                # Save the new Primary key to the dictionary.

                # find the primary key
                for k in new_obj.__dict__.keys():
                    if k.lower() == new_obj.__mapper__.primary_key[0].name:
                        new_pk = new_obj.__dict__[k]
                        # pk = k
                        break
                # new_pk = getattr(new_obj, pk)

                # save pk to dictionary
                self.added_objs[obj] = new_pk

            except Exception as e:
                self._session_out.rollback()
                # print(e)
                # raise e
        # return added

    def fill_dict(self, obj):
        for val in ['SpecimenTypeCV', 'SiteTypeCV', 'CensorCodeCV']:
            try:
                getattr(obj, val)
            except:
                pass

    def get_new_objects(self, obj, valuedict):

        for key in dir(obj):
            if 'obj' in key.lower():  # key.contains('Obj'):
                try:
                    att = getattr(obj, key)

                    objkey = key.replace('Obj', 'ID')
                    if att is not None:
                        valuedict[objkey] = self.added_objs[att]
                    else:
                        valuedict[objkey] = None

                except Exception as e:
                    # print ('cannot find {} in {}. Error:{} in YamlPrinter'.format(key, obj.__class__, e))  # noqa
                    pass

                except Exception as e:
                    print e
                    self._session_out.rollback()
        return valuedict

    # def get_new_objects(self, obj, valuedict):
    #     for key in dir(obj):
    #         if 'obj' in key.lower():  # key.contains('Obj'):
    #             try:
    #                 _changeSchema(None)
    #                 att = getattr(obj, key)
    #                 if att is not None:
    #                     self.fill_dict(obj)
    #                     attdict = att.__dict__.copy()
    #                     for k in attdict.keys():
    #                         if k.lower() == att.__mapper__.primary_key[0].name:
    #
    #                             del attdict[k]
    #                         elif 'obj' in k.lower():
    #                             del attdict[k]
    #                     attdict.pop('_sa_instance_state')
    #                     attdict = self.get_new_objects(att, attdict)
    #
    #                     # model = self.check_model(attr =att)
    #                     model= type(att)
    #                     # new_obj = self._session_out.query(model).filter_by(**attdict).first()
    #                     new_obj = self.get_or_create(self._session_out, model, **attdict)
    #
    #                     objkey = key.replace('Obj', 'ID')
    #                     if objkey == 'RelatedFeatureID':
    #                         newkey = 'SamplingFeatureID'
    #                     elif objkey == 'RelatedActionID':
    #                         newkey = 'ActionID'
    #                     elif 'units' in objkey.lower():
    #                         newkey = 'UnitsID'
    #                     elif 'resultvalue' in objkey.lower():
    #                         newkey = 'ValueID'
    #                     else:
    #                         newkey = objkey
    #                     valuedict[objkey] = getattr(new_obj, newkey)
    #
    #             except Exception as e:
    #                 # print ('cannot find {} in {}. Error:{} in dbOutput'.format(key, obj.__class__.__name__, e))  # noqa
    #                 self._session_out.rollback()
    #     return valuedict

    def get_inherited(self, sess, model, **kwargs):
        uuid = {}
        for key in kwargs.keys():
            if 'uuid' in key.lower():
                uuid[key] = kwargs[key]
                break
        try:
            setSchema(self._engine_out)
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
            new_instance = sess.merge(instance)
            sess.flush()
            return new_instance
