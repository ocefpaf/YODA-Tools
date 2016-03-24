__author__ = 'Choonhan Youn'

from timeseries_dao import TimeseriesXlDao
import datetime
import odm2api.ODM2.models as odm2model
import copy

class TimeseriesYoda(object):

    def __init__(self, xl_file):
        self.tdao = TimeseriesXlDao(xl_file)
        self.template_version = None
        self._references = {}
        self._references_aff = {}
        self._references_sf = {}
        self._references_action = {}
        self._references_faction = {}
        self._references_result = {}
        self._references_tresult = {}

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
        header = self.tdao.get_yoda_header()
        yoda_header += " - {"
        yoda_header += "Version: \"{0}\", ".format(header.YODAVersion)
        yoda_header += "Profile: \"{0}\", ".format(header.TemplateProfile)
        yoda_header += "CreationTool: \"YODAPy {0}\", ".format(header.TemplateVersion)
        self.template_version = header.TemplateVersion
        yoda_header += "DateCreated: \"{0}\", ".format(datetime.datetime.strftime(header.VocabUpdate,'%Y-%m-%d'))
        yoda_header += "DateUpdated: \"{0}\"".format(datetime.datetime.strftime(header.VocabUpdate,'%Y-%m-%d'))
        yoda_header += "}\n"
        return yoda_header.replace('None','NULL')

    def get_dataset(self):
        ds = self.tdao.get_dataset()
        # attrs = self.get_object_attrs('DataSets',"DataSetID")
        attrs = ['DataSetUUID','DataSetTypeCV','DataSetCode','DataSetTitle','DataSetAbstract']
        ds_yaml = "DataSets:\n - &DatasetID0001 {"
        ds_yaml = self.get_odm2model_yaml(ds,attrs,ds_yaml)
        k  = ds_yaml.rfind(',')
        ds_yaml = ds_yaml[:k] + "}\n"
        return ds_yaml.replace('None','NULL')

    def get_datasetresults(self):
        dsr_yaml = "DataSetsResults:\n"
        for key in self._references_result.keys():
            dsr_yaml += " - {DataSetObj: *DatasetID0001, ResultObj: %s}\n" % self._references_result[key]
        return dsr_yaml.replace('None','NULL')

    def get_citation(self):
        ci = self.tdao.get_citation()
        # attrs = self.get_object_attrs('Citations',"CitationID")
        attrs = ['Title','Publisher','PublicationYear','CitationLink','DataSetAbstract']
        ci_yaml = "Citations:\n - &CitationID0001 {"
        ci_yaml = self.get_odm2model_yaml(ci,attrs,ci_yaml)
        k  = ci_yaml.rfind(',')
        ci_yaml = ci_yaml[:k] + "}\n"
        return ci_yaml.replace('None','NULL')

    def get_organizations(self):
        orgs = self.tdao.get_all_organizations()
        # attrs = self.get_object_attrs('Organizations',("ID","Obj"))
        attrs = ['OrganizationTypeCV','OrganizationCode','OrganizationName','OrganizationDescription','OrganizationLink']
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
        return org_yaml.replace('None','NULL')

    def get_people(self):
        people = self.tdao.get_all_people()
        # attrs = self.get_object_attrs('People',"ID")
        attrs = ['PersonFirstName','PersonMiddleName','PersonLastName']
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
        return p_yaml.replace('None','NULL')

    def get_authorlists(self):
        als = self.tdao.get_all_authorlists()
        # attrs = self.get_object_attrs('AuthorLists',"ID")
        attrs = ['CitationObj','PersonObj','AuthorOrder']
        al_yaml = "AuthorLists:\n"
        index = 1
        for al in als:
            al_yaml += ' - &AuthorListID{:0>3d} '.format(index)
            al_yaml += "{"
            # cObj = getattr(al,"Citation")
            pObj = getattr(al,"Person")
            setattr(al,"CitationObj","*CitationID0001")
            for key in self._references.keys():
                if not isinstance(key,basestring):
                    if key.__dict__ == pObj.__dict__:
                        setattr(al,"PersonObj",self._references[key])
                        break
            al_yaml = self.get_odm2model_yaml(al,attrs,al_yaml)
            k  = al_yaml.rfind(',')
            al_yaml = al_yaml[:k] + "}\n"
            index += 1
        return al_yaml.replace('None','NULL')

    def get_datasetcitation(self):
        dsc = self.tdao.get_datasetcitation()
        # attrs = self.get_object_attrs('DataSetCitations',"ID")
        # attrs = ['DataSetObj','CitationObj','RelationshipTypeCV']
        attrs = ['RelationshipTypeCV']
        dsc_yaml = "DataSetCitations:\n"
        dsc_yaml += " - {DataSetObj: *DatasetID0001, CitationObj: *CitationID0001, "
        dsc_yaml = self.get_odm2model_yaml(dsc,attrs,dsc_yaml)
        k  = dsc_yaml.rfind(',')
        dsc_yaml = dsc_yaml[:k] + "}\n"
        return dsc_yaml.replace('None','NULL')

    def get_affiliations(self):
        affs = self.tdao.get_all_affiliations()
        # attrs = self.get_object_attrs('Affiliations',"ID")
        attrs = ['PersonObj','OrganizationObj','IsPrimaryOrganizationContact','AffiliationStartDate','AffiliationEndDate',
                 'PrimaryPhone','PrimaryEmail','PrimaryAddress','PersonLink']
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
                        # self._references.update({key: '*AffiliationID{:0>3d}'.format(index)})
                        self._references_aff[key] = '*AffiliationID{:0>3d}'.format(index)
                        break
            setattr(aff,"OrganizationObj",self._references[orgObj.OrganizationName])
            asd = getattr(aff,'AffiliationStartDate',None)
            if asd:
                asdate = '{:%Y-%m-%d}'.format(asd)
                setattr(aff,'AffiliationStartDate',asdate)
            aed = getattr(aff,'AffiliationEndDate',None)
            if aed:
                aedate = '{:%Y-%m-%d}'.format(aed)
                setattr(aff,'AffiliationEndDate',aedate)
            aff_yaml = self.get_odm2model_yaml(aff,attrs,aff_yaml)
            k  = aff_yaml.rfind(',')
            aff_yaml = aff_yaml[:k] + "}\n"
            index += 1
        return aff_yaml.replace('None','NULL')

    def get_spatialreferences(self):
        srs = self.tdao.get_all_spatialreferences()
        # attrs = self.get_object_attrs('SpatialReferences',"ID")
        attrs = ['SRSCode','SRSName','SRSDescription','SRSLink']
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
        return sr_yaml.replace('None','NULL')

    def get_samplingfeatures(self):
        psfs = self.tdao.get_all_samplingfeatures()
        # attrs = self.get_object_attrs('SamplingFeatures',"ID")
        # attrs.insert(0,"SamplingFeatureUUID")
        attrs = ['SamplingFeatureUUID','SamplingFeatureTypeCV','SamplingFeatureCode','SamplingFeatureName',
                 'SamplingFeatureDescription','SamplingFeatureGeotypeCV','FeatureGeometry','Elevation_m',
                 'ElevationDatumCV']
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
        return sf_yaml.replace('None','NULL')

    def get_sites(self):
        sites = self.tdao.get_all_sites()
        # attrs = self.get_object_attrs('Sites',"ID")
        attrs = ['SamplingFeatureObj','SiteTypeCV','Latitude','Longitude','SpatialReferenceObj']
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
        return site_yaml.replace('None','NULL')

    def get_relatedfeatures(self):
        rfs = self.tdao.get_all_relatedfeatures()
        if rfs is None:
            return None
        # attrs = self.get_object_attrs('RelatedFeatures',"ID")
        attrs = ['SamplingFeatureObj','RelationshipTypeCV','RelatedFeatureObj','SpatialOffsetObj']
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
        return rf_yaml.replace('None','NULL')

    def get_units(self):
        units = self.tdao.get_all_units()
        # attrs = self.get_object_attrs('Units',"ID")
        attrs = ['UnitsTypeCV','UnitsAbbreviation','UnitsName','UnitsLink']
        u_yaml = "Units:\n"
        index = 1
        for u in units:
            uname = getattr(u,"UnitsName")
            self._references[uname] = '*UnitID{:0>3d}'.format(index)
            u_yaml += ' - &UnitID{:0>3d} '.format(index)
            u_yaml += "{"
            u_yaml = self.get_odm2model_yaml(u,attrs,u_yaml)
            k  = u_yaml.rfind(',')
            u_yaml = u_yaml[:k] + "}\n"
            index += 1
        return u_yaml.replace('None','NULL')

    def get_methods(self):
        methods = self.tdao.get_all_methods()
        # attrs = self.get_object_attrs('Methods',"ID")
        attrs = ['MethodTypeCV','MethodCode','MethodName','MethodDescription','MethodLink',
                 'OrganizationObj']
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
        return m_yaml.replace('None','NULL')

    def get_variables(self):
        varis = self.tdao.get_all_variables()
        # attrs = self.get_object_attrs('Variables',"ID")
        attrs = ['VariableTypeCV','VariableCode','VariableNameCV','VariableDefinition','SpeciationCV',
                 'NoDataValue']
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
        return v_yaml.replace('None','NULL')

    def get_processinglevels(self):
        pls = self.tdao.get_all_processinglevels()
        # attrs = self.get_object_attrs('ProcessingLevels',"ID")
        attrs = ['ProcessingLevelCode','Definition','Explanation']
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
        return pl_yaml.replace('None','NULL')

    def get_actions(self):
        actions = self.tdao.get_all_actions()
        action_description = "Generic observation action generated by Excel Template for TimeSeries " + self.template_version
        # attrs = self.get_object_attrs('Actions',"ID")
        attrs = ['ActionTypeCV','MethodObj','BeginDateTime','BeginDateTimeUTCOffset',
                 'EndDateTime','EndDateTimeUTCOffset','ActionDescription','ActionFileLink']
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
            setattr(action,"ActionDescription",action_description)
            a_yaml = self.get_odm2model_yaml(action,attrs,a_yaml)
            k  = a_yaml.rfind(',')
            a_yaml = a_yaml[:k] + "}\n"
            index += 1
        return a_yaml.replace('None','NULL')

    def get_featureactions(self):
        factions = self.tdao.get_all_featureactions()
        # attrs = self.get_object_attrs('FeatureActions',"ID")
        attrs = ['SamplingFeatureObj','ActionObj']
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
                mObj = key.__dict__['Method']
                amObj = aObj.__dict__['Method']
                if key.__dict__["ActionTypeCV"] == aObj.__dict__["ActionTypeCV"] \
                   and key.__dict__["BeginDateTime"] == aObj.__dict__["BeginDateTime"] \
                   and mObj.__dict__['MethodCode'] == amObj.__dict__['MethodCode']:
                    setattr(fa,"ActionObj",self._references_action[key])
                    break
            fa_yaml = self.get_odm2model_yaml(fa,attrs,fa_yaml)
            k  = fa_yaml.rfind(',')
            fa_yaml = fa_yaml[:k] + "}\n"
            index += 1
        return fa_yaml.replace('None','NULL')

    def get_actionbys(self):
        actionbys = self.tdao.get_all_actionbys()
        # attrs = self.get_object_attrs('ActionBy',"ID")
        attrs = ['ActionObj','AffiliationObj','IsActionLead','RoleDescription']
        ab_yaml = "ActionBy:\n"
        for ab in actionbys:
            ab_yaml += ' - {'
            aObj = getattr(ab,"Action")
            for key in self._references_action.keys():
                mObj = key.__dict__['Method']
                amObj = aObj.__dict__['Method']
                if key.__dict__["ActionTypeCV"] == aObj.__dict__["ActionTypeCV"] \
                   and key.__dict__["BeginDateTime"] == aObj.__dict__["BeginDateTime"] \
                   and mObj.__dict__['MethodCode'] == amObj.__dict__['MethodCode']:
                    setattr(ab,"ActionObj",self._references_action[key])
                    break
            affObj = getattr(ab,"Affiliation")
            perObj = getattr(affObj,"Person")
            for key in self._references_aff.keys():
                if not isinstance(key,basestring):
                    if key.__dict__ == perObj.__dict__:
                        setattr(ab,"AffiliationObj",self._references_aff[key])
                        break
            ab_yaml = self.get_odm2model_yaml(ab,attrs,ab_yaml)
            k  = ab_yaml.rfind(',')
            ab_yaml = ab_yaml[:k] + "}\n"
        return ab_yaml.replace('None','NULL')

    def get_results(self):
        results = self.tdao.get_all_results()
        # attrs = self.get_object_attrs('Results',"ID")
        # attrs.insert(0,"ResultUUID")
        attrs = ['ResultUUID','FeatureActionObj','ResultTypeCV','VariableObj','UnitsObj',
                 'TaxonomicClassifierObj','ProcessingLevelObj','ResultDateTime','ResultDateTimeUTCOffset',
                 'ValidDateTime','ValidDateTimeUTCOffset','StatusCV','SampledMediumCV','ValueCount']
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
            uObj = getattr(r,'Unit')
            setattr(r,"UnitsObj",self._references[uObj.UnitsName])
            r_yaml = self.get_odm2model_yaml(r,attrs,r_yaml)
            k  = r_yaml.rfind(',')
            r_yaml = r_yaml[:k] + "}\n"
            index += 1
        return r_yaml.replace('None','NULL')

    def get_timeseriesresults(self):
        tresults = self.tdao.get_all_timeseriesresults()
        # attrs = self.get_object_attrs('TimeSeriesResults',"ID")
        attrs = ['ResultObj','XLocation','XLocationUnitsObj','YLocation','YLocationUnitsObj',
                 'ZLocation','ZLocationUnitsObj','SpatialReferenceObj','IntendedTimeSpacing',
                 'IntendedTimeSpacingUnitsObj','AggregationStatisticCV']
        tr_yaml = "TimeSeriesResults:\n"
        index = 1
        for tr in tresults:
            tr_key = copy.copy(tr)
            self._references_tresult[tr_key] = '*TimeSeriesResultID{:0>3d}'.format(index)
            tr_yaml += ' - &TimeSeriesResultID{:0>3d} '.format(index)
            tr_yaml += "{"
            rObj = getattr(tr,"Result")
            faObj = getattr(rObj,"FeatureAction")
            sfObj = getattr(faObj,'SamplingFeature')
            vObj = getattr(rObj,"Variable")
            for key in self._references_result.keys():
                r_faObj = key.__dict__["FeatureAction"]
                r_sfObj = getattr(r_faObj,"SamplingFeature")
                r_vObj = key.__dict__["Variable"]
                if sfObj.SamplingFeatureCode == r_sfObj.SamplingFeatureCode \
                   and vObj.VariableCode == r_vObj.VariableCode:
                    setattr(tr,"ResultObj",self._references_result[key])
                    break
            srObj = getattr(tr,"SpatialReference",None)
            if srObj and srObj.SRSName:
                setattr(tr,"SpatialReferenceObj",self._references[srObj.SRSName])
            tr_yaml = self.get_odm2model_yaml(tr,attrs,tr_yaml)
            k  = tr_yaml.rfind(',')
            tr_yaml = tr_yaml[:k] + "}\n"
            index += 1
        return tr_yaml.replace('None','NULL')

    def get_timeseriesresultvalues(self):
        trvs = self.tdao.get_all_timeseriesresultvalues()
        datavalue_header = ['ValueDateTime','ValueDateTimeUTCOffset']
        index = 3
        trv_yaml = "TimeSeriesResultValues:\n"
        trv_yaml +=" ColumnDefinitions:\n"
        trv_yaml +="   - {ColumnNumber: 0001, Label: ValueDateTime, ODM2Field: ValueDateTime}\n"
        trv_yaml +="   - {ColumnNumber: 0002, Label: ValueDateTimeUTCOffset, ODM2Field: ValueDateTimeUTCOffset}\n"

        for trv in trvs:
            trv_yaml +="   - {"
            trv_yaml += 'ColumnNumber: {:0>4d}, '.format(index)
            dv_label = getattr(trv,'ColumnLabel')
            datavalue_header.append(dv_label)
            trv_yaml += 'Label: {0}, '.format(dv_label)
            trv_yaml += 'ODM2Field: "DataValue", '
            trObj = getattr(trv,"TimeSeriesResult")
            rObj = getattr(trObj,"Result")
            faObj = getattr(rObj,"FeatureAction")
            sfObj = getattr(faObj,'SamplingFeature')
            vObj = getattr(rObj,"Variable")
            for key in self._references_tresult.keys():
                mr_rObj = key.__dict__["Result"]
                mr_faObj = getattr(mr_rObj,"FeatureAction")
                mr_sfObj = getattr(mr_faObj,"SamplingFeature")
                mr_vObj = getattr(mr_rObj,"Variable")
                if sfObj.SamplingFeatureCode == mr_sfObj.SamplingFeatureCode \
                   and vObj.VariableCode == mr_vObj.VariableCode:
                    trv_yaml += 'Result: {0}, '.format(self._references_tresult[key])
                    break
            trv_yaml += 'CensorCodeCV: {0}, '.format(getattr(trv,'CensorCodeCV'))
            trv_yaml += 'QualityCodeCV: {0}, '.format(getattr(trv,'QualityCodeCV'))
            trv_yaml += 'TimeAggregationInterval: {0}, '.format(getattr(trv,'TimeAggregationInterval'))
            uObj = getattr(trv,'TimeAggregationIntervalUnit')
            trv_yaml += 'TimeAggregationIntervalUnitsObj: {0}'.format(self._references[uObj.UnitsName])
            trv_yaml += "}\n"
            index += 1
        dvalues = self.tdao.get_all_datavalues()
        trv_yaml +=" Data:\n"
        # noU = []
        trv_yaml +="   - [ "
        for d in datavalue_header:
            trv_yaml +="{0}, ".format(d)
            # noU.append(str(d))
        k = trv_yaml.rfind(',')
        trv_yaml = trv_yaml[:k] + " ]\n"
        for dv in dvalues:
            dv_array ="   - [ "
            for dvh in datavalue_header:
                v = getattr(dv,dvh,0)
                if dvh == 'ValueDateTime':
                    v = '"{:%Y-%m-%d %H:%M:%S}"'.format(v)
                elif dvh == 'ValueDateTimeUTCOffset':
                    v = str(int(v))
                else:
                    v = str(v)
                dv_array += v + ", "
            # trv_yaml +='   - {0}\n'.format(dv_array)
            k = dv_array.rfind(',')
            dv_array = dv_array[:k] + " ]\n"
            trv_yaml += dv_array
        return trv_yaml.replace('None','NULL')

    def create_yoda(self,out_file):
        with open(out_file, 'w') as yaml_schema_file:
            yaml_schema_file.write(self.get_header())
            yaml_schema_file.write(self.get_dataset())
            yaml_schema_file.write(self.get_organizations())
            yaml_schema_file.write(self.get_people())
            yaml_schema_file.write(self.get_affiliations())
            yaml_schema_file.write(self.get_citation())
            yaml_schema_file.write(self.get_authorlists())
            yaml_schema_file.write(self.get_datasetcitation())
            yaml_schema_file.write(self.get_spatialreferences())
            yaml_schema_file.write(self.get_samplingfeatures())
            yaml_schema_file.write(self.get_sites())
            yaml_schema_file.write(self.get_units())
            rf = self.get_relatedfeatures()
            if rf:
                yaml_schema_file.write(rf)
            yaml_schema_file.write(self.get_methods())
            yaml_schema_file.write(self.get_variables())
            yaml_schema_file.write(self.get_processinglevels())
            yaml_schema_file.write(self.get_actions())
            yaml_schema_file.write(self.get_featureactions())
            yaml_schema_file.write(self.get_actionbys())
            yaml_schema_file.write(self.get_results())
            yaml_schema_file.write(self.get_datasetresults())
            yaml_schema_file.write(self.get_timeseriesresults())
            yaml_schema_file.write(self.get_timeseriesresultvalues())
