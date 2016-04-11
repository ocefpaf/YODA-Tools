import unittest
from yodatool.generate.measurement.measurement_dao import MeasurementXlDao
import yodatool.generate.measurement.measurement_models as model

class TestMeasurement(unittest.TestCase):

    def setUp(self):
        self.loader = MeasurementXlDao('./yodatool/examples/YODA_Specimen_TEMPLATE_WORKING.xlsm')

    def test_measurement(self):
        # test_affiliations
        affs = self.loader.get_all_affiliations()
        for x in affs:
            print x.__dict__
            perobj = getattr(x,'Person')
            orgobj = getattr(x,'Organization')
            if perobj is not None:
                print perobj.__dict__
            if orgobj is not None:
                print orgobj.__dict__
        self.assertIsInstance(affs[0],model.Affiliation)

        # test_get_dataset(self):
        ds = self.loader.get_dataset()
        if ds:
            print ds.__dict__
            self.assertIsInstance(ds,model.Dataset)

        ci = self.loader.get_citation()
        if ci:
            print ci.__dict__
            self.assertIsInstance(ci,model.Citation)

        dc = self.loader.get_datasetcitation()
        if dc:
            print dc.__dict__
            self.assertIsInstance(dc,model.DataSetCitation)

        # test_authorlists(self):
        al = self.loader.get_all_authorlists()
        if al and len(al):
            for x in al:
                print x.__dict__
                perobj = getattr(x,'Person')
                ciobj = getattr(x,'Citation')
                if perobj is not None:
                    print perobj.__dict__
                if ciobj is not None:
                    print ciobj.__dict__
            self.assertIsInstance(al[0],model.AuthorList)

        # test_samplingfeatures(self):
        sf = self.loader.get_all_samplingfeatures()
        for x in sf:
            print x.__dict__
        self.assertIsInstance(sf[0],model.SamplingFeature)

        # test_sites(self):
        s = self.loader.get_all_sites()
        for x in s:
            print x.__dict__
            sf_obj = getattr(x,'SamplingFeature')
            if sf_obj is not None:
                print sf_obj.__dict__
            sr_obj = getattr(x,'SpatialReference')
            if sr_obj is not None:
                print sr_obj.__dict__
        self.assertIsInstance(s[0],model.Site)

        # test_specimens(self):
        sp = self.loader.get_all_specimens()
        print "specimens size: {0}".format(len(sp))
        if sp is not None:
            print len(sp)
            for x in sp:
                sf_obj = getattr(x,'SamplingFeature')
                print sf_obj.__getattribute__('SamplingFeatureCode'), x.__getattribute__('SpecimenTypeCV')
            self.assertIsInstance(sp[0],model.Specimen)

        # test_spatialoffsets(self):
        soo = self.loader.get_all_spatialoffsets()
        if soo:
            for x in soo:
                print x.__dict__
            self.assertIsInstance(soo[0],model.SpatialOffset)

        # test_relatedfeatures(self):
        rfs = self.loader.get_all_relatedfeatures()
        print "relatedfeature size: {0}".format(len(rfs))
        if rfs is not None:
            print len(rfs)
            for x in rfs:
                sf_obj = getattr(x,'SamplingFeature')
                rf_obj = getattr(x,'RelatedFeature')
                print sf_obj.__dict__
                print rf_obj.__dict__
            self.assertIsInstance(rfs[0],model.RelatedFeature)

        # test_methods(self):
        m = self.loader.get_all_methods()
        for x in m:
            print x.__dict__
            org = getattr(x,'Organization')
            if org is not None:
                print org.__dict__
        self.assertIsInstance(m[0],model.Method)

        # test_actions(self):
        a = self.loader.get_all_actions()
        print "action size: {0}".format(len(a))
        for x in a:
            print x.__dict__
            m = getattr(x,'Method')
            if m is not None:
                print m.__dict__
        self.assertIsInstance(a[0],model.Action)

        # test_actionbys(self):
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
        self.assertIsInstance(ab[0],model.ActionBy)

        # test_featureactions(self):
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
        self.assertIsInstance(fa[0],model.FeatureAction)

        # test_results(self):
        r = self.loader.get_all_results()
        print "result size: {0}".format(len(r))
        for x in r:
            print x.__dict__
            v = getattr(x,'Variable')
            if v is not None:
                print v.__dict__
        self.assertIsInstance(r[0],model.Result)

        # test_measurementresults(self):
        rm = self.loader.get_all_measurementresults()
        print "measurementresult size: {0}".format(len(rm))
        for x in rm:
            print x.__dict__
            r = getattr(x,'Result')
            if r is not None:
                print r.__dict__
        self.assertIsInstance(rm[0],model.MeasurementResult)

        # test_measurementresultvalues(self):
        rmv = self.loader.get_all_measurementresultvalues()
        print "measurementresultvalue size: {0}".format(len(rmv))
        for x in rmv:
            print x.__dict__
            r = getattr(x,'MeasurementResult')
            if r is not None:
                print r.__dict__
        self.assertIsInstance(rmv[0],model.MeasurementResultValue)

        # test_variables(self):
        v = self.loader.get_all_variables()
        for x in v:
            print x.__dict__
        self.assertIsInstance(v[0],model.Variable)

        # test_processinglevels(self):
        pl = self.loader.get_all_processinglevels()
        for x in pl:
            print x.__dict__
        self.assertIsInstance(pl[0],model.ProcessingLevel)

        # test_datacolumns(self):
        datacolumns = self.loader.get_all_datacolumns()
        for dc in datacolumns:
            print dc.__dict__
        self.assertIsInstance(datacolumns[0],model.DataColumn)

        # test_datavalues(self):
        dv = self.loader.get_all_datavalues()
        print "data value size: {0}".format(len(dv))
        # for x in dv:
        #     print x.__dict__
        self.assertIsInstance(dv[0],model.DataValue)

        # test_spatialreferences(self):
        sr = self.loader.get_all_spatialreferences()
        if sr and len(sr) > 0:
            for s in sr:
                print s.__dict__
            self.assertIsInstance(sr[0],model.SpatialReference)

        # test_child_samplingfeatures(self):
        child_sf = self.loader.get_all_child_samplingfeatures()
        if child_sf and len(child_sf):
            print "samplingfeature size: {0}".format(len(child_sf))
            for x in child_sf:
                print x.__dict__
            self.assertIsInstance(child_sf[0],model.SamplingFeature)

if __name__ == '__main__':
    unittest.main()
