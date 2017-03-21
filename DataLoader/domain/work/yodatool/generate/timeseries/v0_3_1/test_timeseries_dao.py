from DataLoader.domain.work.yodatool.generate.timeseries.v0_3_1.timeseries_dao import TimeseriesXlDao

class TestTimeSeriesDao(object):

    def __init__(self,loader):
        self.loader = loader

    def test_get_yoda_header(self):
        yoda_header = self.loader.get_yoda_header()
        if yoda_header:
            print yoda_header.__dict__

    def test_get_all_people(self):
        p = self.loader.get_all_people()
        for x in p:
            print x.__dict__

    def test_get_all_organizations(self):
        o = self.loader.get_all_organizations()
        for x in o:
            print x.__dict__

    def test_get_all_affiliations(self):
        affs = self.loader.get_all_affiliations()
        for x in affs:
            print x.__dict__
            perobj = getattr(x,'Person')
            orgobj = getattr(x,'Organization')
            if perobj is not None:
                print perobj.__dict__
            if orgobj is not None:
                print orgobj.__dict__

    def test_get_dataset_with_citation(self):
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

    def test_spatialoffsets(self):
        soo = self.loader.get_all_spatialoffsets()
        for x in soo:
            print x.__dict__

    def test_relatedfeatures(self):
        rfs = self.loader.get_all_relatedfeatures()
        if rfs is not None:
            for x in rfs:
                print x.__dict__
                sf_obj = getattr(x,'SamplingFeature')
                rf_obj = getattr(x,'RelatedFeature')
                so_obj = getattr(x,'SpatialOffset')
                print sf_obj.__dict__
                print rf_obj.__dict__
                print so_obj.__dict__

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

    def test_timeseriesresults(self):
        tr = self.loader.get_all_timeseriesresults()
        print "timeseries result size: {0}".format(len(tr))
        for x in tr:
            print x.__dict__
            r = getattr(x,'Result')
            if r is not None:
                print r.__dict__

    def test_timeseriesresultvalues(self):
        trv = self.loader.get_all_timeseriesresultvalues()
        print "timeseries result value size: {0}".format(len(trv))
        for x in trv:
            print x.__dict__
            r = getattr(x,'TimeSeriesResult')
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

    def test_units(self):
        u = self.loader.get_all_units()
        for x in u:
            print x.__dict__

    def test_datacolumns(self):
        datacolumns = self.loader.get_all_datacolumns()
        for dc in datacolumns:
            print dc.__dict__

    def test_datavalues(self):
        dv = self.loader.get_all_datavalues()
        print "timeseries dat value size: {0}".format(len(dv))
        # for x in dv:
        #     print x.__dict__
        #     break

    def test_spatialreferences(self):
        sr = self.loader.get_all_spatialreferences()
        for s in sr:
            print s.__dict__

def main():
    #loader = TimeseriesXlDao(excelFile='YODA_TimeSeries_Example1_Template_0.3.1-alpha.xlsm')
    loader = TimeseriesXlDao(excelFile='YODA_v0.3.2_TS_multiple_LR_GC_C.xlsm')
    test = TestTimeSeriesDao(loader)
    # test.test_get_yoda_header()
    # test.test_get_all_people()
    # test.test_get_all_organizations()
    # test.test_get_all_affiliations()
    # test.test_get_dataset_with_citation()
    # test.test_authorlists()
    # test.test_samplingfeatures()
    # test.test_sites()
    # test.test_spatialoffsets()
    # test.test_relatedfeatures()
    # test.test_methods()
    # test.test_variables()
    # test.test_processinglevels()
    # test.test_units()
    # test.test_spatialreferences()
    # test.test_datacolumns()
    # test.test_actions()
    # test.test_actionbys()
    # test.test_featureactions()
    # test.test_results()
    # test.test_timeseriesresults()
    # test.test_timeseriesresultvalues()
    test.test_datavalues()
    loader.close()

if __name__ == '__main__':
    main()
