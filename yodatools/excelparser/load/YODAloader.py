import odm2api.ODM2.models as models
from odm2api.ODMconnection import dbconnection

from YODAqueries import yodaService as yodaservice
from db_schema.create_schema import odm2CreateSchema as odm2schema
from db_schema.cvload import runCVscript as odm2cv

class obj(object):
    def __init__(self, d):
        # for a, b in d.items():
        # for a smaller memory footprint
        for a, b in d.iteritems():
            # if a == 'FeatureGeometry':
            #    b = None
            #    print "F: %s" % b
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)

class yodaLoad():
    def __init__(self):
        self.yoda_service = ''

    def db_setup(self,db_engine,db_name,address=None,
                 user=None,password=None,script_filename=None):
        odm2model = odm2schema()
        # create schema
        if db_engine == 'sqlite':
            conn_string = odm2model.getconnectionstring(db_engine,db_name)
            odm2model.runSQLiteScript(script_filename,db_name)
            odm2cv(conn_string)
            conn = dbconnection.createConnection(db_engine, db_name)
            self.yoda_service = yodaservice(conn)
        elif db_engine == 'postgresql':
            conn_string = odm2model.getconnectionstring(db_engine,address,db_name,user,password)
            odm2model.runPostgeSQLScript(db_name,address,user,password,script_filename)
            odm2cv(conn_string)
            conn = dbconnection.createConnection(db_engine,address,db_name,user,password)
            self.yoda_service = yodaservice(conn)
        else:
            print "other database type is not supported yet........"

    def getOrganization(self, model, org):
        if hasattr(org, 'OrganizationObj'):
            print "Parent organization is existed!!! Currently it is not used"
            setattr(org, 'ParentOrganizationID', None)
            delattr(org, 'OrganizationObj')
        else:
            setattr(org, 'ParentOrganizationID', None)
        return self.yoda_service.get_or_createObject(model, org)

    def getExternalIdentifierSystems(self, model, eis):
        org = getattr(models, 'Organizations')
        org = self.getOrganization(org, eis.IdentifierSystemOrganizationObj)
        setattr(eis, 'IdentifierSystemOrganizationID', org.OrganizationID)
        delattr(eis, 'IdentifierSystemOrganizationObj')
        return self.yoda_service.get_or_createObject(model, eis)

    def getPersonExternalIdentifiers(self, model, pei):
        p = getattr(models, 'People')
        person = self.yoda_service.get_or_createObject(p, pei.PersonObj)
        e = getattr(models, 'ExternalIdentifierSystems')
        eis = self.getExternalIdentifierSystems(e, pei.ExternalIdentifierSystemObj)
        setattr(pei, 'PersonID', person.PersonID)
        setattr(pei, 'ExternalIdentifierSystemID', eis.ExternalIdentifierSystemID)
        delattr(pei, 'ExternalIdentifierSystemObj')
        delattr(pei, 'PersonObj')
        return self.yoda_service.get_or_createObject(model, pei)

    def getAffiliations(self, model, aff):
        p = getattr(models, 'People')
        person = self.yoda_service.get_or_createObject(p, aff.PersonObj)
        if aff.OrganizationObj != None:
            org = getattr(models, 'Organizations')
            org = self.getOrganization(org, aff.OrganizationObj)
            setattr(aff, 'OrganizationID', org.OrganizationID)
        else:
            setattr(aff, 'OrganizationID', None)
        setattr(aff, 'PersonID', person.PersonID)
        delattr(aff, 'OrganizationObj')
        delattr(aff, 'PersonObj')
        return self.yoda_service.get_or_createObject(model, aff)

    def getAuthorLists(self, model, al):
        c = getattr(models, 'Citations')
        c = self.yoda_service.get_or_createObject(c, al.CitationObj)
        p = getattr(models, 'People')
        person = self.yoda_service.get_or_createObject(p, al.PersonObj)
        setattr(al, 'PersonID', person.PersonID)
        setattr(al, 'CitationID', c.CitationID)
        delattr(al, 'PersonObj')
        delattr(al, 'CitationObj')
        return self.yoda_service.get_or_createObject(model, al)

    def getDatasetCitations(self, model, dc):
        c = getattr(models, 'Citations')
        c = self.yoda_service.get_or_createObject(c, dc.CitationObj)
        setattr(dc, 'CitationID', c.CitationID)
        delattr(dc, 'CitationObj')
        ds = getattr(models, 'DataSets')
        ds = self.yoda_service.get_or_createObject(ds, dc.DataSetObj)
        setattr(dc, 'DataSetID', ds.DataSetID)
        delattr(dc, 'DataSetObj')
        return self.yoda_service.get_or_createObject(model, dc)

    def getSamplingFeatureExternalIdentifiers(self, model, sfei):
        sf = getattr(models, 'SamplingFeatures')
        sf = self.yoda_service.get_or_createObject(sf, sfei.SamplingFeatureObj)
        setattr(sfei, 'SamplingFeatureID', sf.SamplingFeatureID)
        delattr(sfei, 'SamplingFeatureObj')
        eis = getattr(models, 'ExternalIdentifierSystems')
        eis = self.getExternalIdentifierSystems(eis, sfei.ExternalIdentifierSystemObj)
        setattr(sfei, 'ExternalIdentifierSystemID', eis.ExternalIdentifierSystemID)
        delattr(sfei, 'ExternalIdentifierSystemObj')
        return self.yoda_service.get_or_createObject(model, sfei)

    def getCitationExternalIdentifiers(self, model, cei):
        c = getattr(models, 'Citations')
        c = self.yoda_service.get_or_createObject(c, cei.CitationObj)
        setattr(cei, 'CitationID', c.CitationID)
        delattr(cei, 'CitationObj')

        eis = getattr(models, 'ExternalIdentifierSystems')
        eis = self.getExternalIdentifierSystems(eis, cei.ExternalIdentifierSystemObj)
        setattr(cei, 'ExternalIdentifierSystemID', eis.ExternalIdentifierSystemID)
        delattr(cei, 'ExternalIdentifierSystemObj')
        return self.yoda_service.get_or_createObject(model, cei)

    def getSites(self, model, site):
        sf = getattr(models, 'SamplingFeatures')
        sf = self.yoda_service.get_or_createObject(sf, site.SamplingFeatureObj)
        setattr(site, 'SamplingFeatureID', sf.SamplingFeatureID)
        delattr(site, 'SamplingFeatureObj')
        sr = getattr(models, 'SpatialReferences')
        sr = self.yoda_service.get_or_createObject(sr, site.SpatialReferenceObj)
        setattr(site, 'SpatialReferenceID', sr.SpatialReferenceID)
        delattr(site, 'SpatialReferenceObj')
        return self.yoda_service.get_or_createObject(model, site)

    def getSpecimens(self, model, sp):
        sf = getattr(models, 'SamplingFeatures')
        sf = self.yoda_service.get_or_createObject(sf, sp.SamplingFeatureObj)
        setattr(sp, 'SamplingFeatureID', sf.SamplingFeatureID)
        delattr(sp, 'SamplingFeatureObj')
        return self.yoda_service.get_or_createObject(model, sp)

    def getSpatialOffsets(self, model, so):
        uobj = getattr(models, 'Units')
        if so.Offset1UnitObj == None:
            setattr(so, 'Offset1UnitID', None)
        else:
            u = self.yoda_service.get_or_createObject(uobj, so.Offset1UnitObj)
            setattr(so, 'Offset1UnitID', u.UnitsID)
        if so.Offset2UnitObj == None:
            setattr(so, 'Offset2UnitID', None)
        else:
            u = self.yoda_service.get_or_createObject(uobj, so.Offset2UnitObj)
            setattr(so, 'Offset2UnitID', u.UnitsID)
        if so.Offset3UnitObj == None:
            setattr(so, 'Offset3UnitID', None)
        else:
            u = self.yoda_service.get_or_createObject(uobj, so.Offset3UnitObj)
            setattr(so, 'Offset3UnitID', u.UnitsID)
        delattr(so, 'Offset1UnitObj')
        delattr(so, 'Offset2UnitObj')
        delattr(so, 'Offset3UnitObj')
        return self.yoda_service.get_or_createObject(model, so)

    def getRelatedFeatures(self, model, rf):
        sfobj = getattr(models, 'SamplingFeatures')
        sf = self.yoda_service.get_or_createObject(sfobj, rf.SamplingFeatureObj)
        setattr(rf, 'SamplingFeatureID', sf.SamplingFeatureID)
        sf = self.yoda_service.get_or_createObject(sfobj, rf.RelatedFeatureObj)
        setattr(rf, 'RelatedFeatureID', sf.SamplingFeatureID)
        if rf.SpatialOffsetObj != None:
            so = getattr(models, 'SpatialOffsets')
            so = self.getSpatialOffsets(so, rf.SpatialOffsetObj)
            setattr(rf, 'SpatialOffsetID', so.SpatialOffsetID)
        else:
            setattr(rf, 'SpatialOffsetID', None)
        delattr(rf, 'SamplingFeatureObj')
        delattr(rf, 'RelatedFeatureObj')
        delattr(rf, 'SpatialOffsetObj')
        return self.yoda_service.get_or_createObject(model, rf)

    def getMethod(self, model, method):
        if hasattr(method, 'OrganizationObj'):
            if method.OrganizationObj != None:
                org = getattr(models, 'Organizations')
                org = self.getOrganization(org, method.OrganizationObj)
                setattr(method, 'OrganizationID', org.OrganizationID)
            else:
                setattr(method, 'OrganizationID', None)
            delattr(method, 'OrganizationObj')
        else:
            setattr(method, 'OrganizationID', None)
        return self.yoda_service.get_or_createObject(model, method)

    def getAction(self, model, action):
        m = getattr(models, 'Methods')
        m = self.getMethod(m, action.MethodObj)
        setattr(action, 'MethodID', m.MethodID)
        delattr(action, 'MethodObj')
        at = self.yoda_service.get_or_createObject(model, action)
        return at

    def getFeatureAction(self, model, fa):
        sf = getattr(models, 'SamplingFeatures')
        sf = self.yoda_service.get_or_createObject(sf, fa.SamplingFeatureObj)
        setattr(fa, 'SamplingFeatureID', sf.SamplingFeatureID)
        delattr(fa, 'SamplingFeatureObj')
        a = getattr(models, 'Actions')
        a = self.getAction(a, fa.ActionObj)
        setattr(fa, 'ActionID', a.ActionID)
        delattr(fa, 'ActionObj')

        return self.yoda_service.get_or_createObject(model, fa)

    def getActionBy(self,model, aby):
        a = getattr(models, 'Actions')
        a = self.getAction(a, aby.ActionObj)
        setattr(aby, 'ActionID', a.ActionID)
        delattr(aby, 'ActionObj')
        af = getattr(models, 'Affiliations')
        af = self.getAffiliations(af, aby.AffiliationObj)
        setattr(aby, 'AffiliationID', af.AffiliationID)
        delattr(aby, 'AffiliationObj')

        # if aby.IsActionLead:
        #    setattr(aby,"IsActionLead",1)
        # else:
        #    setattr(aby,"IsActionLead",0)

        return self.yoda_service.get_or_createObject(model, aby)


    def getResults(self,model, r):
        fa = getattr(models, 'FeatureActions')
        fa = self.getFeatureAction(fa, r.FeatureActionObj)
        setattr(r, 'FeatureActionID', fa.FeatureActionID)
        delattr(r, 'FeatureActionObj')
        v = getattr(models, 'Variables')
        v = self.yoda_service.get_or_createObject(v, r.VariableObj)
        setattr(r, 'VariableID', v.VariableID)
        delattr(r, 'VariableObj')
        if r.UnitsObj == None:
            setattr(r, 'UnitsID', None)
        else:
            u = getattr(models, 'Units')
            u = self.yoda_service.get_or_createObject(u, r.UnitsObj)
            setattr(r, 'UnitsID', u.UnitsID)
        delattr(r, 'UnitsObj')

        if r.TaxonomicClassifierObj == None:
            setattr(r, 'TaxonomicClassifierID', None)
        else:
            t = getattr(models, 'TaxonomicClassifiers')
            t = self.yoda_service.get_or_createTaxonomicclassifier(t, r.TaxonomicClassifierObj)
            setattr(r, 'TaxonomicClassifierID', t.TaxonomicClassifierID)
        delattr(r, 'TaxonomicClassifierObj')
        p = getattr(models, 'ProcessingLevels')
        p = self.yoda_service.get_or_createObject(p, r.ProcessingLevelObj)
        setattr(r, 'ProcessingLevelID', p.ProcessingLevelID)
        delattr(r, 'ProcessingLevelObj')
        return self.yoda_service.get_or_createObject(model, r)


    def getDatasetsResults(self,model, ds):
        d = getattr(models, 'DataSets')
        d = self.yoda_service.get_or_createObject(d, ds.DataSetObj)
        setattr(ds, 'DataSetID', d.DataSetID)
        delattr(ds, 'DataSetObj')
        r = getattr(models, 'Results')
        r = self.getResults(r, ds.ResultObj)
        setattr(ds, 'ResultID', r.ResultID)
        delattr(ds, 'ResultObj')
        return self.yoda_service.get_or_createObject(model, ds)


    def getDataResults(self,model, dr, dataType):
        r = getattr(models, 'Results')
        r = self.getResults(r, dr.ResultObj)
        setattr(dr, 'ResultID', r.ResultID)
        delattr(dr, 'ResultObj')

        uobj = getattr(models, 'Units')
        if dr.XLocationUnitsObj == None:
            setattr(dr, 'XLocationUnitsID', None)
        else:
            u = self.yoda_service.get_or_createObject(uobj, dr.XLocationUnitsObj)
            setattr(dr, 'XLocationUnitsID', u.UnitsID)
        if dr.YLocationUnitsObj == None:
            setattr(dr, 'YLocationUnitsID', None)
        else:
            u = self.yoda_service.get_or_createObject(uobj, dr.YLocationUnitsObj)
            setattr(dr, 'YLocationUnitsID', u.UnitsID)
        if dr.ZLocationUnitsObj == None:
            setattr(dr, 'ZLocationUnitsID', None)
        else:
            u = self.yoda_service.get_or_createObject(uobj, dr.ZLocationUnitsObj)
            setattr(dr, 'ZLocationUnitsID', u.UnitsID)

        delattr(dr, 'XLocationUnitsObj')
        delattr(dr, 'YLocationUnitsObj')
        delattr(dr, 'ZLocationUnitsObj')

        if dr.SpatialReferenceObj == None:
            setattr(dr, 'SpatialReferenceID', None)
        else:
            sr = getattr(models, 'SpatialReferences')
            sr = self.yoda_service.get_or_createObject(sr, dr.SpatialReferenceObj)
            setattr(dr, 'SpatialReferenceID', sr.SpatialReferenceID)
        delattr(dr, 'SpatialReferenceObj')

        if dataType == 'TimeSeries':
            if dr.IntendedTimeSpacingUnitsObj == None:
                setattr(dr, 'IntendedTimeSpacingUnitsID', None)
            else:
                u = self.yoda_service.get_or_createObject(uobj, dr.IntendedTimeSpacingUnitsObj)
                setattr(dr, 'IntendedTimeSpacingUnitsID', u.UnitsID)
            delattr(dr, 'IntendedTimeSpacingUnitsObj')

        if dataType == 'Measurement':
            u = self.yoda_service.get_or_createObject(uobj, dr.TimeAggregationIntervalUnitsObj)
            setattr(dr, 'TimeAggregationIntervalUnitsID', u.UnitsID)
            delattr(dr, 'TimeAggregationIntervalUnitsObj')

        return self.yoda_service.get_or_createObject(model, dr)


    def getTimeSeriesResultValues(self,trv, valueDateTime, valueDateTimeUTCOffset, dataValue):
        ts = getattr(models, 'TimeSeriesResults')
        ts = self.getDataResults(ts, trv.Result, 'TimeSeries')
        setattr(trv, 'ResultID', ts.ResultID)
        delattr(trv, 'Result')
        delattr(trv, 'ColumnNumber')
        delattr(trv, 'ODM2Field')
        u = getattr(models, 'Units')
        u = self.yoda_service.get_or_createObject(u, trv.TimeAggregationIntervalUnitsObj)
        setattr(trv, 'TimeAggregationIntervalUnitsID', u.UnitsID)
        delattr(trv, 'TimeAggregationIntervalUnitsObj')
        setattr(trv, 'ValueDateTime', None)
        setattr(trv, 'ValueDateTimeUTCOffset', None)
        setattr(trv, 'DataValue', None)
        return self.yoda_service.get_or_createTimeSeriesResultValues(trv, valueDateTime, valueDateTimeUTCOffset, dataValue)


    def getMeasurementResultValues(self,model, mrv):
        ms = getattr(models, 'MeasurementResults')
        ms = self.getDataResults(ms, mrv.MeasurementResultObj, 'Measurement')
        setattr(mrv, 'ResultID', ms.ResultID)
        delattr(mrv, 'MeasurementResultObj')
        return self.yoda_service.get_or_createObject(model, mrv)


    def data_load(self,dataMap):
        s = obj(dataMap)

        for attr, value in s.__dict__.iteritems():
            # print attr,value
            if attr == 'Organizations':
                print "Organization:=============="
                for x in value:
                    org = getattr(models, attr)
                    org = self.getOrganization(org, x)
                    print "OrganizationID:", org.OrganizationID

            elif attr == 'ExternalIdentifierSystems':
                print "ExternalIdentifierSystems:============"
                for x in value:
                    eis = getattr(models, attr)
                    eis = self.getExternalIdentifierSystems(eis, x)
                    print "ExternalIdentifierSystemID:", eis.ExternalIdentifierSystemID

            elif attr == 'PersonExternalIdentifiers':
                print "PersonExternalIdentifiers:=========="
                for x in value:
                    pei = getattr(models, attr)
                    pei = self.getPersonExternalIdentifiers(pei, x)
                    print "BridgeID:", pei.BridgeID

            elif attr == 'Affiliations':
                print "Affiliations:==========="
                for x in value:
                    a = getattr(models, attr)
                    a = self.getAffiliations(a, x)
                    print "AffiliationID:", a.AffiliationID

            elif attr == 'AuthorLists':
                print "AuthorLists:=============="
                for x in value:
                    a = getattr(models, attr)
                    a = self.getAuthorLists(a, x)
                    print "BridgeID:", a.BridgeID

            elif attr == 'DataSetCitations':
                print "DataSetCitations:================="
                for x in value:
                    dc = getattr(models, attr)
                    dc = self.getDatasetCitations(dc, x)
                    print "BridgeID:", dc.BridgeID

            elif attr == 'SamplingFeatureExternalIdentifiers':
                print "SamplingFeatureExternalIdentifiers:=========="
                for x in value:
                    sfei = getattr(models, attr)
                    sfei = self.getSamplingFeatureExternalIdentifiers(sfei, x)
                    print "BridgeID:", sfei.BridgeID
            # specimens measurement
            elif attr == 'CitationExternalIdentifiers':
                print "CitationExternalIdentifiers:=========="
                for x in value:
                    cei = getattr(models, attr)
                    cei = self.getCitationExternalIdentifiers(cei, x)
                    print "BridgeID:", cei.BridgeID

            elif attr == 'Sites':
                print "Sites:=============="
                for x in value:
                    site = getattr(models, attr)
                    site = self.getSites(site, x)
                    print "SamplingFeatureID:", site.SamplingFeatureID

            elif attr == 'Specimens':
                print "Specimens:================="
                for x in value:
                    sp = getattr(models, attr)
                    sp = self.getSpecimens(sp, x)
                    print "SamplingFeatureID:", sp.SamplingFeatureID

            elif attr == 'SpatialOffsets':
                print "SpatialOffsets:============="
                for x in value:
                    so = getattr(models, attr)
                    so = self.getSpatialOffsets(so, x)
                    print "SpatialOffsetID:", so.SpatialOffsetID

            elif attr == 'RelatedFeatures':
                print "RelatedFeatures:==========="
                for x in value:
                    rf = getattr(models, attr)
                    rf = self.getRelatedFeatures(rf, x)
                    print "RelationID:", rf.RelationID

            elif attr == 'Methods':
                print "Methods:=============="
                for x in value:
                    m = getattr(models, attr)
                    m = self.getMethod(m, x)
                    print "MethodID:", m.MethodID

            elif attr == 'Actions':
                print "Actions:==============="
                for x in value:
                    a = getattr(models, attr)
                    a = self.getAction(a, x)
                    print "ActionID:", a.ActionID

            elif attr == 'FeatureActions':
                print "FeatureActions:=============="
                for x in value:
                    fa = getattr(models, attr)
                    fa = self.getFeatureAction(fa, x)
                    print "FeatureActionID:", fa.FeatureActionID

            elif attr == 'ActionBy':
                print "ActionBy:================="
                for x in value:
                    aby = getattr(models, attr)
                    aby = self.getActionBy(aby, x)
                    print "BridgeID:", aby.ActionID

            elif attr == 'Results':
                print "Results:============"
                for x in value:
                    rt = getattr(models, attr)
                    rt = self.getResults(rt, x)
                    print "ResultID:", rt.ResultID

            elif attr == 'DataSetsResults':
                print "DataSetsResults:============="
                for x in value:
                    ds = getattr(models, attr)
                    ds = self.getDatasetsResults(ds, x)
                    print "BridgeID:", ds.BridgeID

            elif attr == 'TimeSeriesResults':
                print "TimeSeriesResults:=========="
                for x in value:
                    tr = getattr(models, attr)
                    tr = self.getDataResults(tr, x, 'TimeSeries')
                    print "Time Series ResultID:", tr.ResultID

            elif attr == 'TimeSeriesResultValues':
                print "TimeSeriesResultValues:=========="
                valuelist = [[] for i in xrange(len(value.ColumnDefinitions))]
                print "valuelist", len(valuelist)
                for x in value.Data:
                    for i in range(len(x)):
                        #for j in range(len(x[i])):
                        valuelist[i].append(x[i])

                for x in value.ColumnDefinitions:
                    if hasattr(x, 'Result'):
                        trv = self.getTimeSeriesResultValues(x, valuelist[0], valuelist[1], valuelist[x.ColumnNumber - 1])
                        print "ValueID:", trv.ValueID
            elif attr == 'MeasurementResults':
                print "MeasurementResults:=========="
                for x in value:
                    mr = getattr(models, attr)
                    mr = self.getDataResults(mr, x, 'Measurement')
                    print "Measure ResultID:", mr.ResultID

            elif attr == 'MeasurementResultValues':
                print "MeasurementResultValues:=========="
                for x in value:
                    mrv = getattr(models, attr)
                    mrv = self.getMeasurementResultValues(mrv, x)


            else:
                print "%s:==============" % attr
                if attr == 'YODA':
                    continue
                for x in value:
                    ds = getattr(models, attr)
                    ds = self.yoda_service.get_or_createObject(ds, x)
                    if attr == 'DataSets':
                        print "DataSetID:", ds.DataSetID
                    if attr == 'People':
                        print "PersonID:", ds.PersonID
                    if attr == 'Citations':
                        print "CitationID:", ds.CitationID
                    if attr == 'SpatialReferences':
                        print "SpatialReferenceID:", ds.SpatialReferenceID
                    if attr == 'SamplingFeatures':
                        print "SamplingFeatureID:", ds.SamplingFeatureID
                    if attr == 'Variables':
                        print "VariableID:", ds.VariableID
                    if attr == 'ProcessingLevels':
                        print "ProcessingLevelID:", ds.ProcessingLevelID

