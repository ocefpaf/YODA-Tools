__author__ = 'Choonhan Youn'

from measurement_dao import MeasurementXlDao
import datetime
import odm2api.ODM2.models as odm2model
import copy

class MeasurementYoda(object):

    def __init__(self, xl_file):
        self.mdao = MeasurementXlDao(xl_file)
        self._references = {}
        self._references_sf = {}
        self._references_action = {}
        self._references_faction = {}
        self._references_result = {}
        self._references_mresult = {}

    def get_object_attrs(self,obj,filters=None):
        obj = getattr(odm2model,obj)
        if filters is not None:
            return [i for i in obj.__dict__.keys() if i[:1] != '_' and not i.endswith(filters)]
        else:
            return [i for i in obj.__dict__.keys() if i[:1] != '_']

    def get_odm2model_yaml(self,cls,attrs,yaml_text):
        for attr in attrs:
            value = getattr(cls,attr,None)
            if isinstance(value,basestring) and not value.startswith('*'):
                yaml_text += "{0}: \"{1}\", ".format(attr, value.encode('utf-8'))
            elif isinstance(value,datetime.datetime):
                yaml_text += "{0}: \"{1}\", ".format(attr, value)
            else:
                yaml_text += "{0}: {1}, ".format(attr, value)
        return yaml_text

    def get_header(self):
        yoda_header = "---\n"
        yoda_header +="YODA:\n"
        header = self.mdao.get_yoda_header()
        yoda_header += " - {"
        yoda_header += "Version: \"{0}\", ".format(header.YODAVersion)
        yoda_header += "Profile: \"{0}\", ".format(header.TemplateProfile)
        yoda_header += "CreationTool: YODAPy \"{0}\", ".format(header.TemplateVersion)
        yoda_header += "DateCreated: \"{0}\", ".format(datetime.datetime.strftime(header.VocabUpdate,'%Y-%m-%d'))
        yoda_header += "DateUpdated: \"{0}\"".format(datetime.datetime.strftime(header.VocabUpdate,'%Y-%m-%d'))
        yoda_header += "}\n"
        return yoda_header

    def get_dataset(self):
        ds = self.mdao.get_dataset()
        attrs = self.get_object_attrs('DataSets',"DataSetID")
        ds_yaml = "DataSets:\n - &DatasetID0001 {"
        ds_yaml = self.get_odm2model_yaml(ds,attrs,ds_yaml)
        k  = ds_yaml.rfind(',')
        ds_yaml = ds_yaml[:k] + "}\n"
        return ds_yaml

    def get_organizations(self):
        orgs = self.mdao.get_all_organizations()
        attrs = self.get_object_attrs('Organizations',("ID","Obj"))
        org_yaml = "Organizations:\n"
        index = 1
        for org in orgs:
            orgname = getattr(org,"OrganizationName")
            self._references[orgname] = '*OrganizationID{:0>3d}'.format(index)
            org_yaml += ' - &OrganizationID{:0>3d} '.format(index)
            org_yaml += "{"
            org_yaml = self.get_odm2model_yaml(org,attrs,org_yaml)
            k  = org_yaml.rfind(',')
            org_yaml = org_yaml[:k] + "}\n"
            index += 1
        return org_yaml

    def get_people(self):
        people = self.mdao.get_all_people()
        attrs = self.get_object_attrs('People',"ID")
        p_yaml = "People:\n"
        index = 1
        for p in people:
            self._references[p] = '*PersonID{:0>3d}'.format(index)
            p_yaml += ' - &PersonID{:0>3d} '.format(index)
            p_yaml += "{"
            p_yaml = self.get_odm2model_yaml(p,attrs,p_yaml)
            k  = p_yaml.rfind(',')
            p_yaml = p_yaml[:k] + "}\n"
            index += 1
        return p_yaml

    def get_affiliations(self):
        affs = self.mdao.get_all_affiliations()
        attrs = self.get_object_attrs('Affiliations',"ID")
        aff_yaml = "Affiliations:\n"
        index = 1
        for aff in affs:
            aff_yaml += ' - &AffiliationID{:0>3d} '.format(index)
            aff_yaml += "{"
            orgObj = getattr(aff,"Organization")
            perObj = getattr(aff,"Person")
            for key in self._references.keys():
                if not isinstance(key,basestring):
                    if key.__dict__ == perObj.__dict__:
                        setattr(aff,"PersonObj",self._references[key])
                        self._references.update({key: '*AffiliationID{:0>3d}'.format(index)})
                        break
            setattr(aff,"OrganizationObj",self._references[orgObj.OrganizationName])
            aff_yaml = self.get_odm2model_yaml(aff,attrs,aff_yaml)
            k  = aff_yaml.rfind(',')
            aff_yaml = aff_yaml[:k] + "}\n"
            index += 1
        return aff_yaml

    def get_spatialreferences(self):
        srs = self.mdao.get_all_spatialreferences()
        attrs = self.get_object_attrs('SpatialReferences',"ID")
        sr_yaml = "SpatialReferences:\n"
        index = 1
        for sr in srs:
            srname = getattr(sr,"SRSName")
            self._references[srname] = '*SpatialReferenceID{:0>3d}'.format(index)
            sr_yaml += ' - &SpatialReferenceID{:0>3d} '.format(index)
            sr_yaml += "{"
            sr_yaml = self.get_odm2model_yaml(sr,attrs,sr_yaml)
            k  = sr_yaml.rfind(',')
            sr_yaml = sr_yaml[:k] + "}\n"
            index += 1
        return sr_yaml

    def get_samplingfeatures(self):
        psfs = self.mdao.get_all_samplingfeatures()
        csfs = self.mdao.get_all_child_samplingfeatures()
        attrs = self.get_object_attrs('SamplingFeatures',"ID")
        attrs.insert(0,"SamplingFeatureUUID")
        sf_yaml = "SamplingFeatures:\n"
        index = 1
        for psf in psfs:
            sfcode = getattr(psf,"SamplingFeatureCode")
            self._references_sf[sfcode] = '*SamplingFeatureID{:0>3d}'.format(index)
            sf_yaml += ' - &SamplingFeatureID{:0>3d} '.format(index)
            sf_yaml += "{"
            sf_yaml = self.get_odm2model_yaml(psf,attrs,sf_yaml)
            k  = sf_yaml.rfind(',')
            sf_yaml = sf_yaml[:k] + "}\n"
            index += 1

        for csf in csfs:
            sfcode = getattr(csf,"SamplingFeatureCode")
            self._references_sf[sfcode] = '*SamplingFeatureID{:0>3d}'.format(index)
            sf_yaml += ' - &SamplingFeatureID{:0>3d} '.format(index)
            sf_yaml += "{"
            sf_yaml = self.get_odm2model_yaml(csf,attrs,sf_yaml)
            k  = sf_yaml.rfind(',')
            sf_yaml = sf_yaml[:k] + "}\n"
            index += 1
        return sf_yaml

    def get_sites(self):
        sites = self.mdao.get_all_sites()
        attrs = self.get_object_attrs('Sites',"ID")
        site_yaml = "Sites:\n"
        for site in sites:
            site_yaml += ' - {'
            sfObj = getattr(site,"SamplingFeature")
            srObj = getattr(site,"SpatialReference")
            setattr(site,"SamplingFeatureObj",self._references_sf[sfObj.SamplingFeatureCode])
            setattr(site,"SpatialReferenceObj",self._references[srObj.SRSName])
            site_yaml = self.get_odm2model_yaml(site,attrs,site_yaml)
            k  = site_yaml.rfind(',')
            site_yaml = site_yaml[:k] + "}\n"
        return site_yaml

    def get_specimens(self):
        specimens = self.mdao.get_all_specimens()
        attrs = self.get_object_attrs('Specimens',"ID")
        specimen_yaml = "Specimens:\n"
        for specimen in specimens:
            specimen_yaml += ' - {'
            sfObj = getattr(specimen,"SamplingFeature")
            setattr(specimen,"SamplingFeatureObj",self._references_sf[sfObj.SamplingFeatureCode])
            specimen_yaml = self.get_odm2model_yaml(specimen,attrs,specimen_yaml)
            k  = specimen_yaml.rfind(',')
            specimen_yaml = specimen_yaml[:k] + "}\n"
        return specimen_yaml

    def get_relatedfeatures(self):
        rfs = self.mdao.get_all_relatedfeatures()
        attrs = self.get_object_attrs('RelatedFeatures',"ID")
        rf_yaml = "RelatedFeatures:\n"
        for rf in rfs:
            rf_yaml += ' - {'
            sfObj = getattr(rf,"SamplingFeature")
            rfObj = getattr(rf,"RelatedFeature")
            #soObj = getattr(rf,"SpatialOffset")
            setattr(rf,"SamplingFeatureObj",self._references_sf[sfObj.SamplingFeatureCode])
            setattr(rf,"RelatedFeatureObj",self._references_sf[rfObj.SamplingFeatureCode])
            #setattr(rf,"SpatialOffsetObj",self._references_sf[soObj.SpatialOffsetCode])
            rf_yaml = self.get_odm2model_yaml(rf,attrs,rf_yaml)
            k  = rf_yaml.rfind(',')
            rf_yaml = rf_yaml[:k] + "}\n"
        return rf_yaml

    def get_methods(self):
        methods = self.mdao.get_all_methods()
        attrs = self.get_object_attrs('Methods',"ID")
        m_yaml = "Methods:\n"
        index = 1
        for m in methods:
            mcode = getattr(m,"MethodCode")
            self._references[mcode] = '*MethodID{:0>3d}'.format(index)
            m_yaml += ' - &MethodID{:0>3d} '.format(index)
            m_yaml += "{"
            orgObj = getattr(m,"Organization")
            if orgObj:
                orgname = orgObj.OrganizationName
                if orgname:
                    setattr(m,"OrganizationObj",self._references[orgname])
            m_yaml = self.get_odm2model_yaml(m,attrs,m_yaml)
            k  = m_yaml.rfind(',')
            m_yaml = m_yaml[:k] + "}\n"
            index += 1
        return m_yaml

    def get_variables(self):
        varis = self.mdao.get_all_variables()
        attrs = self.get_object_attrs('Variables',"ID")
        v_yaml = "Variables:\n"
        index = 1
        for v in varis:
            vcode = getattr(v,"VariableCode")
            self._references[vcode] = '*VariableID{:0>3d}'.format(index)
            v_yaml += ' - &VariableID{:0>3d} '.format(index)
            v_yaml += "{"
            v_yaml = self.get_odm2model_yaml(v,attrs,v_yaml)
            k  = v_yaml.rfind(',')
            v_yaml = v_yaml[:k] + "}\n"
            index += 1
        return v_yaml

    def get_processinglevels(self):
        pls = self.mdao.get_all_processinglevels()
        attrs = self.get_object_attrs('ProcessingLevels',"ID")
        pl_yaml = "ProcessingLevels:\n"
        index = 1
        for pl in pls:
            pcode = getattr(pl,"ProcessingLevelCode")
            self._references[pcode] = '*ProcessingLevelID{:0>3d}'.format(index)
            pl_yaml += ' - &ProcessingLevelID{:0>3d} '.format(index)
            pl_yaml += "{"
            pl_yaml = self.get_odm2model_yaml(pl,attrs,pl_yaml)
            k  = pl_yaml.rfind(',')
            pl_yaml = pl_yaml[:k] + "}\n"
            index += 1
        return pl_yaml

    def get_actions(self):
        actions = self.mdao.get_all_actions()
        attrs = self.get_object_attrs('Actions',"ID")
        a_yaml = "Actions:\n"
        index = 1
        for action in actions:
            action_key = copy.copy(action)
            self._references_action[action_key] = '*ActionID{:0>3d}'.format(index)
            a_yaml += ' - &ActionID{:0>3d} '.format(index)
            a_yaml += "{"
            mObj = getattr(action,"Method")
            mcode = mObj.MethodCode
            setattr(action,"MethodObj",self._references[mcode])
            a_yaml = self.get_odm2model_yaml(action,attrs,a_yaml)
            k  = a_yaml.rfind(',')
            a_yaml = a_yaml[:k] + "}\n"
            index += 1
        return a_yaml

    def get_featureactions(self):
        factions = self.mdao.get_all_featureactions()
        attrs = self.get_object_attrs('FeatureActions',"ID")
        fa_yaml = "FeatureActions:\n"
        index = 1
        for fa in factions:
            fa_key = copy.copy(fa)
            self._references_faction[fa_key] = '*FeatureActionID{:0>3d}'.format(index)
            fa_yaml += ' - &FeatureActionID{:0>3d} '.format(index)
            fa_yaml += "{"
            sfObj = getattr(fa,"SamplingFeature")
            sfcode = sfObj.SamplingFeatureCode
            setattr(fa,"SamplingFeatureObj",self._references_sf[sfcode])
            aObj = getattr(fa,"Action")
            for key in self._references_action.keys():
                if key.__dict__["ActionTypeCV"] == aObj.__dict__["ActionTypeCV"] \
                   and key.__dict__["BeginDateTime"] == aObj.__dict__["BeginDateTime"]:
                    setattr(fa,"ActionObj",self._references_action[key])
                    break
            fa_yaml = self.get_odm2model_yaml(fa,attrs,fa_yaml)
            k  = fa_yaml.rfind(',')
            fa_yaml = fa_yaml[:k] + "}\n"
            index += 1
        return fa_yaml

    def get_actionbys(self):
        actionbys = self.mdao.get_all_actionbys()
        attrs = self.get_object_attrs('ActionBy',"ID")
        ab_yaml = "ActionBy:\n"
        for ab in actionbys:
            ab_yaml += ' - {'
            aObj = getattr(ab,"Action")
            for key in self._references_action.keys():
                if key.__dict__["ActionTypeCV"] == aObj.__dict__["ActionTypeCV"] \
                   and key.__dict__["BeginDateTime"] == aObj.__dict__["BeginDateTime"]:
                    setattr(ab,"ActionObj",self._references_action[key])
                    break
            affObj = getattr(ab,"Affiliation")
            perObj = getattr(affObj,"Person")
            for key in self._references.keys():
                if not isinstance(key,basestring):
                    if key.__dict__ == perObj.__dict__:
                        setattr(ab,"AffiliationObj",self._references[key])
                        break
            ab_yaml = self.get_odm2model_yaml(ab,attrs,ab_yaml)
            k  = ab_yaml.rfind(',')
            ab_yaml = ab_yaml[:k] + "}\n"
        return ab_yaml

    def get_results(self):
        results = self.mdao.get_all_results()
        attrs = self.get_object_attrs('Results',"ID")
        attrs.insert(0,"ResultUUID")
        r_yaml = "Results:\n"
        index = 1
        for r in results:
            r_key = copy.copy(r)
            self._references_result[r_key] = '*ResultID{:0>3d}'.format(index)
            r_yaml += ' - &ResultID{:0>3d} '.format(index)
            r_yaml += "{"
            faObj = getattr(r,"FeatureAction")
            sfObj = getattr(faObj,'SamplingFeature')
            aObj = getattr(faObj,"Action")
            for key in self._references_faction.keys():
                f_sfObj = key.__dict__["SamplingFeature"]
                f_aObj = key.__dict__["Action"]
                if sfObj.SamplingFeatureCode == f_sfObj.SamplingFeatureCode \
                   and aObj.BeginDateTime == f_aObj.BeginDateTime:
                    setattr(r,"FeatureActionObj",self._references_faction[key])
                    break
            vObj = getattr(r,"Variable")
            setattr(r,"VariableObj",self._references[vObj.VariableCode])
            plObj = getattr(r,"ProcessingLevel")
            setattr(r,"ProcessingLevelObj",self._references[plObj.ProcessingLevelCode])
            setattr(r,"UnitsObj",r.Unit)
            r_yaml = self.get_odm2model_yaml(r,attrs,r_yaml)
            k  = r_yaml.rfind(',')
            r_yaml = r_yaml[:k] + "}\n"
            index += 1
        return r_yaml

    def get_measurementresults(self):
        mresults = self.mdao.get_all_measurementresults()
        attrs = self.get_object_attrs('MeasurementResults',"ID")
        mr_yaml = "MeasurementResults:\n"
        index = 1
        for mr in mresults:
            mr_key = copy.copy(mr)
            self._references_mresult[mr_key] = '*MeasurementResultID{:0>3d}'.format(index)
            mr_yaml += ' - &MeasurementResultID{:0>3d} '.format(index)
            mr_yaml += "{"
            rObj = getattr(mr,"Result")
            faObj = getattr(rObj,"FeatureAction")
            sfObj = getattr(faObj,'SamplingFeature')
            vObj = getattr(rObj,"Variable")
            for key in self._references_result.keys():
                r_faObj = key.__dict__["FeatureAction"]
                r_sfObj = getattr(r_faObj,"SamplingFeature")
                r_vObj = key.__dict__["Variable"]
                if sfObj.SamplingFeatureCode == r_sfObj.SamplingFeatureCode \
                   and vObj.VariableCode == r_vObj.VariableCode:
                    setattr(mr,"ResultObj",self._references_result[key])
                    break
            srObj = getattr(mr,"SpatialReference",None)
            if srObj and srObj.SRSName:
                setattr(mr,"SpatialReferenceObj",self._references[srObj.SRSName])
            setattr(mr,"TimeUnitObj",mr.TimeAggregationIntervalUnitsID)
            mr_yaml = self.get_odm2model_yaml(mr,attrs,mr_yaml)
            k  = mr_yaml.rfind(',')
            mr_yaml = mr_yaml[:k] + "}\n"
            index += 1
        return mr_yaml

    def get_measurementresultvalues(self):
        mrvs = self.mdao.get_all_measurementresultvalues()
        attrs = self.get_object_attrs('MeasurementResultValues',"ID")
        mrv_yaml = "MeasurementResultValues:\n"
        for mrv in mrvs:
            mrv_yaml += " - {"
            mrObj = getattr(mrv,"MeasurementResult")
            rObj = getattr(mrObj,"Result")
            faObj = getattr(rObj,"FeatureAction")
            sfObj = getattr(faObj,'SamplingFeature')
            vObj = getattr(rObj,"Variable")
            for key in self._references_mresult.keys():
                mr_rObj = key.__dict__["Result"]
                mr_faObj = getattr(mr_rObj,"FeatureAction")
                mr_sfObj = getattr(mr_faObj,"SamplingFeature")
                mr_vObj = getattr(mr_rObj,"Variable")
                if sfObj.SamplingFeatureCode == mr_sfObj.SamplingFeatureCode \
                   and vObj.VariableCode == mr_vObj.VariableCode:
                    setattr(mrv,"MeasurementResultObj",self._references_mresult[key])
                    break
            mrv_yaml = self.get_odm2model_yaml(mrv,attrs,mrv_yaml)
            k  = mrv_yaml.rfind(',')
            mrv_yaml = mrv_yaml[:k] + "}\n"
        return mrv_yaml

    def create_yoda(self,out_file):
        with open(out_file, 'w') as yaml_schema_file:
            yaml_schema_file.write(self.get_header())
            yaml_schema_file.write(self.get_dataset())
            yaml_schema_file.write(self.get_organizations())
            yaml_schema_file.write(self.get_people())
            yaml_schema_file.write(self.get_affiliations())
            yaml_schema_file.write(self.get_spatialreferences())
            yaml_schema_file.write(self.get_samplingfeatures())
            yaml_schema_file.write(self.get_sites())
            yaml_schema_file.write(self.get_specimens())
            yaml_schema_file.write(self.get_relatedfeatures())
            yaml_schema_file.write(self.get_methods())
            yaml_schema_file.write(self.get_variables())
            yaml_schema_file.write(self.get_processinglevels())
            yaml_schema_file.write(self.get_actions())
            yaml_schema_file.write(self.get_featureactions())
            yaml_schema_file.write(self.get_actionbys())
            yaml_schema_file.write(self.get_results())
            yaml_schema_file.write(self.get_measurementresults())
            yaml_schema_file.write(self.get_measurementresultvalues())
