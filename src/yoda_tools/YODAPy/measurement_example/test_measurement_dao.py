from measurement_dao import MeasurementXlDao

class TestMeasurementDao(object):

    def __init__(self,loader):
        self.loader = loader

    def test_aaffiliations(self):
        affs = self.loader.get_all_affiliations()
        for x in affs:
            print x.__dict__
            perobj = getattr(x,'Person')
            orgobj = getattr(x,'Organization')
            if perobj is not None:
                print perobj.__dict__
            if orgobj is not None:
                print orgobj.__dict__

    def test_personexternalidentifiers(self):
        pe = self.loader.get_all_personexternalidentifiers()
        for x in pe:
            print x.__dict__
            perobj = getattr(x,'Person')
            eisobj = getattr(x,'ExternalIdentifierSystem')
            if perobj is not None:
                print perobj.__dict__
            if eisobj is not None:
                print eisobj.__dict__

    def test_get_dataset(self):
        ds = self.loader.get_dataset()
        if ds:
            print ds.__dict__
        ci = self.loader.get_citation()
        if ci:
            print ci.__dict__
        dc = self.loader.get_datasetcitation()
        if dc:
            print dc.__dict__

    def test_authorlists(self):
        al = self.loader.get_all_authorlists()
        for x in al:
            print x.__dict__
            perobj = getattr(x,'Person')
            ciobj = getattr(x,'Citation')
            if perobj is not None:
                print perobj.__dict__
            if ciobj is not None:
                print ciobj.__dict__

    def test_samplingfeatures(self):
        sf = self.loader.get_all_samplingfeatures()
        for x in sf:
            print x.__dict__

    def test_sites(self):
        s = self.loader.get_all_sites()
        for x in s:
            print x.__dict__
            sf_obj = getattr(x,'SamplingFeature')
            if sf_obj is not None:
                print sf_obj.__dict__
            sr_obj = getattr(x,'SpatialReference')
            if sr_obj is not None:
                print sr_obj.__dict__

    def test_specimens(self):
        sp = self.loader.get_all_specimens()
        print "specimens size: {0}".format(len(sp))
        if sp is not None:
            print len(sp)
            for x in sp:
                sf_obj = getattr(x,'SamplingFeature')
                print sf_obj.__getattribute__('SamplingFeatureCode'), x.__getattribute__('SpecimenTypeCV')

    def test_spatialoffsets(self):
        soo = self.loader.get_all_spatialoffsets()
        for x in soo:
            print x.__dict__

    def test_relatedfeatures(self):
        rfs = self.loader.get_all_relatedfeatures()
        print "relatedfeature size: {0}".format(len(rfs))
        if rfs is not None:
            print len(rfs)
            for x in rfs:
                sf_obj = getattr(x,'SamplingFeature')
                rf_obj = getattr(x,'RelatedFeature')
                print sf_obj.__dict__
                print rf_obj.__dict__

    def test_methods(self):
        m = self.loader.get_all_methods()
        for x in m:
            print x.__dict__
            org = getattr(x,'Organization')
            if org is not None:
                print org.__dict__

    def test_actions(self):
        a = self.loader.get_all_actions()
        print "action size: {0}".format(len(a))
        for x in a:
            print x.__dict__
            m = getattr(x,'Method')
            if m is not None:
                print m.__dict__

    def test_actionbys(self):
        ab = self.loader.get_all_actionbys()
        print "actionby size: {0}".format(len(ab))
        for x in ab:
            print x.__dict__
            a = getattr(x,'Action')
            if a is not None:
                print a.__dict__
            aff = getattr(x,'Affiliation')
            if aff is not None:
                print aff.__dict__

    def test_featureactions(self):
        fa = self.loader.get_all_featureactions()
        print "featureaction size: {0}".format(len(fa))
        for x in fa:
            print x.__dict__
            sf = getattr(x,'SamplingFeature')
            a = getattr(x,'Action')
            if sf is not None:
                print sf.__dict__
            if a is not None:
                print a.__dict__

    def test_results(self):
        r = self.loader.get_all_results()
        print "result size: {0}".format(len(r))
        for x in r:
            print x.__dict__
            v = getattr(x,'Variable')
            if v is not None:
                print v.__dict__

    def test_measurementresults(self):
        rm = self.loader.get_all_measurementresults()
        print "measurementresult size: {0}".format(len(rm))
        for x in rm:
            print x.__dict__
            r = getattr(x,'Result')
            if r is not None:
                print r.__dict__

    def test_measurementresultvalues(self):
        rmv = self.loader.get_all_measurementresultvalues()
        print "measurementresultvalue size: {0}".format(len(rmv))
        for x in rmv:
            print x.__dict__
            r = getattr(x,'Result')
            if r is not None:
                print r.__dict__

    def test_variables(self):
        v = self.loader.get_all_variables()
        for x in v:
            print x.__dict__

    def test_processinglevels(self):
        pl = self.loader.get_all_processinglevels()
        for x in pl:
            print x.__dict__

    def test_datacolumns(self):
        datacolumns = self.loader.get_all_datacolumns()
        for dc in datacolumns:
            print dc.__dict__

    def test_datavalues(self):
        dv = self.loader.get_all_datavalues()
        for x in dv:
            print x.__dict__

    def test_spatialreferences(self):
        sr = self.loader.get_all_spatialreferences()
        for s in sr:
            print s.__dict__

    def test_externalidentifiers(self):
        eid = self.loader.get_all_externalidentifiers()
        for e in eid:
            print e.__dict__
            org_obj = getattr(e,'IdentifierSystemOrganization')
            if org_obj is not None:
                print org_obj.__dict__

    def test_child_samplingfeatures(self):
        child_sf = self.loader.get_all_child_samplingfeatures()
        print "samplingfeature size: {0}".format(len(child_sf))
        for x in child_sf:
            print x.__dict__

def main():
    loader = MeasurementXlDao(excelFile='YODA_Specimen_TEMPLATE_WORKING.xlsm')
    test = TestMeasurementDao(loader)
    #test.test_aaffiliations()
    #test.test_samplingfeatures()
    test.test_sites()
    test.test_variables()
    #test.test_methods()
    #test.test_datavalues()
    loader.close()

if __name__ == '__main__':
    main()
