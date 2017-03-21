import sys

import xlwings as xw

import measurement_models as model
from DataLoader.domain.work.yodatool import BaseXldao

wb = None
Sheet_Names = {
    "1": "Instructions",
    "2": "People and Organizations",
    "3": 'Dataset Citation',
    "4": 'Sampling Features',
    "5": 'Spatial Offsets',
    "6": "Related Features (optional)",
    "7": 'Methods',
    "8": 'Variables',
    "9": 'Processing Levels',
    "10": 'Taxonomic Classifiers',
    "11": 'Data Columns',
    "12": 'Data Values',
    "13": 'Specimen Column Finder', #not working, "SpecimenColumnFinder"
    "14": 'Result Column Labels', #named_range, "ResultColumnLabels"
    "15": 'Result Column Finder', #not working, "ResultColumnFinder"
    "16": 'YODA Header Blocks', #not working
    "17": 'YODA Generator',
    "18": 'YODA File',
    "19": 'Controlled Vocabularies', #named_range, "ControlledVocabularies"
    "20": 'Units',
    "21": 'SpatialReferences',
    "22": 'ExternalIdentifierSystems'
}
Specimen_Comlun_Finder = [
    'DataType',
    'ODM Table',
    'CV Name',
    'REQUIRED',
    'VBV or Column',
    'Data Columns Input Column',
    'Data Values Column Number',
    'Num Required',
    'Num Given',
    'Error?',
    'First Value Address',
    'First Value'
]

Result_Column_Finder = [
    'DataType',
    'ODM Table',
    'CV Name',
    'REQUIRED',
    'VBV or Column',
    'DV Num',
    'Data Value Label',
    'Concat',
    'Concat2',
    'Data Columns Input Column',
    'Data Values Input Row',
    'Data Values Column Number',
    'Num Required',
    'Num Given',
    'Error?',
    'First Value Address',
    'First Value'
]

Column_Names = [
    'DataType',
    'FirstValueAddress',
    'DataValuesColumnNumber',
    'DataColumnsInputColumn',
    'DVNum'
]
DataType_Names = [
    'SpecimenCollector', #0
    'CollectionMethodCode', #1
    'CollectionDateTime', #2
    'CollectionDateTimeUTCOffset', #3
    'ParentSamplingFeatureCode', #4
    'SpatialOffsetCode', #5
    'RelationshipTypeCV', #6
    'SpecimenCode', #7
    'SpecimenDescription', #8
    'SpecimenName', #9
    'SpecimenUUID', #10
    'SpecimenIGSN', #11
    'IsFieldSpecimen', #12
    'SpecimenMediumCV', #13
    'SpecimenTypeCV', #14
    'AnalysisMethodCode', #15
    'AnalysisDateTime', #16
    'AnalysisDateTimeUTCOffset', #17
    'ProcessingLevelCode' #18
]
FirstValueAddress_Names = [
    'Data Values',
    'Data Columns',
    'NOT GIVEN'
]

class MeasurementXlDao(BaseXldao):

    def __init__(self, excelFile=None):
        p = sys.path
        self.wb = xw.Workbook(fullname=p[0] + '/'+excelFile)

    def close(self):
        if wb is not None:
            self.wb.close()

    def printNamedRange(self):
        print self.wb.names
        for e in self.wb.names:
            print e

    def getSheetNames(self):
        return xw.Sheet.all(self.wb)

    # YODA metadata
    def get_yoda_header(self):
        sheet = xw.Sheet(Sheet_Names["1"])
        if sheet is None:
            return None

        YODAVersion = xw.Range(sheet,'YODAVersion').value
        TemplateProfile = xw.Range(sheet,'TemplateProfile').value
        TemplateVersion = xw.Range(sheet,'TemplateVersion').value
        VocabUpdate = xw.Range(sheet,'VocabUpdate').value
        yh_list = [YODAVersion,TemplateProfile,TemplateVersion,VocabUpdate]
        if any(yh_list):
            yh = model.YODAHeader(yh_list)
            return yh
        else:
            return None

    def get_people_dictionary(self):
        sheet = xw.Sheet(Sheet_Names["2"])
        if sheet is None:
            return None

        people = xw.Range(sheet,"People").table.value
        if people is None:
            return None
        peopleResults = {}
        for x in people:
            if any(x):
                if x[1] is not None: #check middle name
                    p_name = '%s %s %s' % (x[0],x[1],x[2])
                else:
                    p_name = '%s %s' % (x[0],x[2])
                perObj = model.Person(x[0:3])
                peopleResults.update({p_name: perObj})
        return peopleResults

    def get_all_people(self):
        sheet = xw.Sheet(Sheet_Names["2"])
        if sheet is None:
            return None

        people = xw.Range(sheet,"People").table.value
        if people is None:
            return None
        peopleResults = []
        for x in people:
            if any(x):
                peopleResults.append(model.Person(x[0:3]))
        return peopleResults

    def get_all_organizations(self):
        sheet = xw.Sheet(Sheet_Names["2"])
        if sheet is None:
            return None

        orgs = xw.Range(sheet,"Organizations").table.value
        if orgs is None:
            return None

        orgResults = []
        for x in orgs:
            if any(x):
                orgResults.append(model.Organization(x))

        external_orgs = self.get_all_externalidorgs()
        if external_orgs is not None and len(external_orgs) > 0:
            for x in external_orgs:
                orgResults.append(x)
        return orgResults

    def get_all_externalidorgs(self):
        sheet = xw.Sheet(Sheet_Names["22"])
        if sheet is None:
            return None
        eidorg = xw.Range(sheet,'ExternalIDOrgs').value
        eidorgResults = []
        for e in eidorg:
            if any(e):
                eidorgResults.append(model.Organization(e))
        return eidorgResults

    def get_externalidentifier_by_name(self,name):
        sheet = xw.Sheet(Sheet_Names["22"])
        if sheet is None:
            return None

        eid = xw.Range(sheet,'ExternalIdentifiers').value
        eidResult = None
        for e in eid:
            if any(e):
                if e[0] == name:
                    orgObj = None
                    if e[1] is not None: #org name
                        orgObj = model.Organization()
                        orgObj.OrganizationName = e[1]
                    e_list = [e[0],e[2],e[3],e[4],orgObj]
                    eidResult = model.ExternalIdentifierSystem(e_list)
                    break
        return eidResult

    def get_all_externalidentifiers(self):
        sheet = xw.Sheet(Sheet_Names["22"])
        if sheet is None:
            return None

        eid = xw.Range(sheet,'ExternalIdentifiers').value
        eidResults = []
        for e in eid:
            if any(e):
                orgObj = None
                if e[1] is not None: #org name
                    orgObj = model.Organization()
                    orgObj.OrganizationName = e[1]
                e_list = [e[0],e[2],e[3],e[4],orgObj]
                eidResults.append(model.ExternalIdentifierSystem(e_list))
        return eidResults

    def get_all_affiliations(self):
        sheet = xw.Sheet(Sheet_Names["2"])
        if sheet is None:
            return None

        people = xw.Range(sheet,"People").table.value
        if people is None:
            return None

        aResults = []
        for x in people:
            if any(x):
                perObj = model.Person()
                perObj.PersonFirstName = x[0]
                perObj.PersonMiddleName = x[1]
                perObj.PersonLastName = x[2]
                orgObj = model.Organization()
                orgObj.OrganizationName = x[3]
                affObj = model.Affiliation()
                affObj.Organization = orgObj
                affObj.Person = perObj
                affObj.PrimaryEmail = x[4]
                affObj.PrimaryAddress = x[5]
                aResults.append(affObj)
        return aResults

    def get_affiliations_dictionary(self):
        sheet = xw.Sheet(Sheet_Names["2"])
        if sheet is None:
            return None

        people = xw.Range(sheet,"People").table.value
        if people is None:
            return None

        aResults = {}
        for x in people:
            if any(x):
                if x[1] is not None: #check middle name
                    p_name = '%s %s %s' % (x[0],x[1],x[2])
                else:
                    p_name = '%s %s' % (x[0],x[2])
                perObj = model.Person()
                perObj.PersonFirstName = x[0]
                perObj.PersonMiddleName = x[1]
                perObj.PersonLastName = x[2]
                orgObj = model.Organization()
                orgObj.OrganizationName = x[3]
                affObj = model.Affiliation()
                affObj.Organization = orgObj
                affObj.Person = perObj
                affObj.PrimaryEmail = x[4]
                affObj.PrimaryAddress = x[5]
                aResults.update({p_name: affObj})
        return aResults

    def get_all_personexternalidentifiers(self):
        sheet = xw.Sheet(Sheet_Names["2"])
        if sheet is None:
            return None

        NumORCIDs = xw.Range(sheet,'NumORCIDs').value
        if NumORCIDs is None or NumORCIDs < 0:
            return None

        people = xw.Range(sheet,"People").table.value
        if people is None:
            return None

        peResults = []
        for x in people:
            if any(x):
                if x[6] is not None:
                    perObj = model.Person(x[0:3])
                    eisObj = model.ExternalIdentifierSystem()
                    eisObj = self.get_externalidentifier_by_name('ORCID')
                    peURI = '%s%s' % (eisObj.ExternalIdentifierSystemURL,x[6])
                    pe_list = [x[6],peURI,perObj,eisObj]
                    peResults.append(model.PersonExternalIdentifier(pe_list))
        return peResults

    def get_dataset(self):
        sheet = xw.Sheet(Sheet_Names["3"])
        if sheet is None:
            return None

        DatasetUUID = xw.Range(sheet,"DatasetUUID").value
        DatasetType = xw.Range(sheet,"DatasetType").value
        DatasetCode = xw.Range(sheet,"DatasetCode").value
        DatasetTitle = xw.Range(sheet,"DatasetTitle").value
        DatasetAbstract = xw.Range(sheet,"DatasetAbstract").value
        ds_list = [DatasetUUID,DatasetType,DatasetCode,DatasetTitle,DatasetAbstract]
        if any(ds_list):
            ds = model.Dataset(ds_list)
            return ds
        else:
            return None

    def get_citation(self):
        sheet = xw.Sheet(Sheet_Names["3"])
        if sheet is None:
            return None

        CitationTitle = xw.Range(sheet,"CitationTitle").value
        Publisher = xw.Range(sheet,"Publisher").value
        PublicationYear = xw.Range(sheet,"PublicationYear").value
        CitationLink = xw.Range(sheet,"CitationLink").value
        ec_list = [CitationTitle,
                   Publisher,
                   PublicationYear,
                   CitationLink]
        if any(ec_list):
            ec = model.Citation(ec_list)
            return ec
        else:
            return None

    def get_datasetcitation(self):
        sheet = xw.Sheet(Sheet_Names["3"])
        if sheet is None:
            return None

        DatasetCitationRelationship = xw.Range(sheet,"DatasetCitationRelationship").value
        if DatasetCitationRelationship is None:
            return None
        Dataset = self.get_dataset()
        Citation = self.get_citation()
        ec_list = [DatasetCitationRelationship,Dataset,Citation]
        if any(ec_list):
            ec = model.DataSetCitation(ec_list)
            return ec
        else:
            return None

    def get_all_authorlists(self):
        sheet = xw.Sheet(Sheet_Names["3"])
        if sheet is None:
            return None
        NumAuthors = xw.Range(sheet,'NumAuthors').value
        if NumAuthors is None or NumAuthors < 0:
            return None

        authors = xw.Range(sheet,"AuthorList").table.value
        if authors is None:
            return None

        Citation = self.get_citation()
        Person_dict = self.get_people_dictionary()
        authorResults = []
        for x in authors:
            if any(x):
                Person = Person_dict.get(x[1])
                au_list = [x[0],Citation,Person]
                authorResults.append(model.AuthorList(au_list))
        return authorResults

    def get_all_samplingfeatures(self):
        sheet = xw.Sheet(Sheet_Names["4"])
        if sheet is None:
            return None

        ElevationDatum = xw.Range(sheet,'ElevationDatum').value
        NumParentSamplingFeatures = xw.Range(sheet,'NumParentSamplingFeatures').value
        if NumParentSamplingFeatures is not None and NumParentSamplingFeatures > 0:
            samplingfeatures = xw.Range(sheet,'SamplingFeatures').value
            sfResults = []
            for sf in samplingfeatures:
                if any(sf):
                    sf.insert(8,ElevationDatum)
                    sfResults.append(model.SamplingFeature(sf[0:9]))
            return sfResults
        else:
            return None

    def get_all_sites(self):
        sheet = xw.Sheet(Sheet_Names["4"])
        if sheet is None:
            return None

        ElevationDatum = xw.Range(sheet,'ElevationDatum').value
        LatLonDatum = xw.Range(sheet,'LatLonDatum').value
        sr_obj = model.SpatialReference()
        sr_obj.SRSName = LatLonDatum

        NumSites = xw.Range(sheet,'NumSites').value
        if NumSites is not None and NumSites > 0:
            samplingfeatures = xw.Range(sheet,'SamplingFeatures').value
            sResults = []
            for sf in samplingfeatures:
                if any(sf):
                    site = [sf[11],sf[12],sf[13]]
                    if any(site):
                        sf.insert(8,ElevationDatum)
                        sf_obj = model.SamplingFeature(sf[0:9])
                        s = [sf[12],sf[13],sf[14],sf_obj,sr_obj]
                        sResults.append(model.Site(s))
            return sResults
        else:
            return None

    def get_all_specimens(self):
        sheet = xw.Sheet(Sheet_Names["4"])
        if sheet is None:
            return None

        spResults = []
        ElevationDatum = xw.Range(sheet,'ElevationDatum').value
        NumParentSpecimens = xw.Range(sheet,'NumParentSpecimens').value
        if NumParentSpecimens is not None and NumParentSpecimens > 0:
            samplingfeatures = xw.Range(sheet,'SamplingFeatures').value
            for sf in samplingfeatures:
                if any(sf):
                    specimen = [sf[15],sf[16],sf[17]]
                    if any(specimen):
                        sf.insert(8,ElevationDatum)
                        sf_obj = model.SamplingFeature(sf[0:9])
                        sp = [sf[16],sf[17],sf[18],sf_obj]
                        spResults.append(model.Specimen(sp))

        scf_list = self.get_all_specimencolumnfinder()
        if scf_list is None:
            if len(spResults) < 0:
                return None
            else:
                return spResults

        sp_codes = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[7])
        sp_desc = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[8])
        sp_name = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[9])
        sp_uuid = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[10])

        IsFieldSpecimen = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[12])
        SpecimenMediumCV = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[13])
        SpecimenTypeCV = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[14])

        for code,stype in zip(sp_codes, SpecimenTypeCV):
            sf_obj = model.SamplingFeature()
            sf_obj.SamplingFeatureUUID = sp_uuid
            sf_obj.SamplingFeatureCode = str(code)
            sf_obj.SamplingFeatureName = sp_name
            sf_obj.SamplingFeatureDescription = sp_desc
            sp = [stype,SpecimenMediumCV,IsFieldSpecimen,sf_obj]
            spResults.append(model.Specimen(sp))

        return spResults

    def get_all_spatialoffsets(self):
        sheet = xw.Sheet(Sheet_Names["5"])
        if sheet is None:
            return None

        SpatialOffsets = xw.Range(sheet,'SpatialOffsets').value
        soResults = []
        for so in SpatialOffsets:
            if any(so):
                soResults.append(model.SpatialOffset(so))
        return soResults

    def get_all_relatedfeatures(self):
        sheet = xw.Sheet(Sheet_Names["6"])
        if sheet is None:
            return None

        rfResults = []
        NumRelatedFeatures = xw.Range(sheet,'NumRelatedFeatures').value
        if NumRelatedFeatures is not None and NumRelatedFeatures > 0:
            RelatedFeatures = xw.Range(sheet,'RelatedFeatures').value
            for rf in RelatedFeatures:
                if any(rf):
                    first_sfObj = model.SamplingFeature()
                    first_sfObj.SamplingFeatureCode = rf[0]
                    second_sfObj = model.SamplingFeature()
                    second_sfObj.SamplingFeatureCode = rf[2]
                    so_obj = None
                    if rf[3] is not None:
                        so_obj = model.SpatialOffset()
                        so_obj.SpatialOffsetCode = rf[3]
                    rf_list = [rf[1],first_sfObj,second_sfObj,so_obj]
                    rfResults.append(model.RelatedFeature(rf_list))

        scf_list = self.get_all_specimencolumnfinder()
        if scf_list is None:
            if len(rfResults) < 0:
                return None
            else:
                return rfResults

        sp_codes = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[7])
        sp_desc = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[8])
        sp_name = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[9])
        sp_uuid = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[10])

        ParentSamplingFeatureCode = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[4])
        SpatialOffsetCode = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[5])
        RelationshipTypeCV = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[6])
        if RelationshipTypeCV is None:
            RelationshipTypeCV = "isChildOf"

        for c_code,p_code in zip(sp_codes, ParentSamplingFeatureCode):
            parent_sfObj = model.SamplingFeature()
            parent_sfObj.SamplingFeatureCode = p_code
            child_sfObj = model.SamplingFeature()
            child_sfObj.SamplingFeatureCode = str(c_code)
            child_sfObj.SamplingFeatureUUID = sp_uuid
            child_sfObj.SamplingFeatureName = sp_name
            child_sfObj.SamplingFeatureDescription = sp_desc
            rf_list = [RelationshipTypeCV,child_sfObj,parent_sfObj,SpatialOffsetCode]
            rfResults.append(model.RelatedFeature(rf_list))

        return rfResults

    def get_all_actions(self):
        aResults = []
        scf_list = self.get_all_specimencolumnfinder()
        if scf_list is not None:
            CollectionMethodCode = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[1])
            CollectionDateTime = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[2])
            CollectionDateTimeUTCOffset = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[3])
            activetypecv = "Specimen collection"
            for m_code,c_time,c_offset in zip(CollectionMethodCode, CollectionDateTime,CollectionDateTimeUTCOffset):
                mObj = model.Method()
                mObj.MethodCode = m_code
                aObj = model.Action()
                aObj.ActionTypeCV = activetypecv
                aObj.BeginDateTime = c_time
                aObj.BeginDateTimeUTCOffset = c_offset
                aObj.Method = mObj
                aResults.append(aObj)

        dc_list = self.get_all_datacolumns()
        if dc_list is not None:
            analysisdatetime = None
            AnalysisDateTimeUTCOffset = None
            AnalysisMethodCode = None

            for dc in dc_list:
                ColumnType = getattr(dc,'ColumnType')
                if ColumnType == 'AnalysisDateTime':
                    adt_col = getattr(dc,'ColumnNumber')
                    analysisdatetime = self.get_datavalues_by_column(adt_col)
                    atc_value = getattr(dc,'AppliesToColumn')
                    for x in dc_list:
                        col_label = getattr(x,'ColumnLabel')
                        if col_label == atc_value:
                            AnalysisMethodCode = getattr(x,'AnalysisMethodCode')
                            break
                if ColumnType == 'AnalysisDateTimeUTCOffset':
                    adto_col = getattr(dc,'ColumnNumber')
                    AnalysisDateTimeUTCOffset = self.get_datavalues_by_column(adto_col)

            mObj = model.Method()
            mObj.MethodCode = AnalysisMethodCode
            activetypecv = "Specimen analysis"
            for adt,adto in zip(analysisdatetime,AnalysisDateTimeUTCOffset):
                aObj = model.Action()
                aObj.ActionTypeCV = activetypecv
                aObj.BeginDateTime = adt
                aObj.BeginDateTimeUTCOffset = adto
                aObj.Method = mObj
                aResults.append(aObj)
        return aResults

    def get_all_actionbys(self):
        aResults = []
        scf_list = self.get_all_specimencolumnfinder()
        if scf_list is not None:
            CollectionMethodCode = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[1])
            CollectionDateTime = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[2])
            CollectionDateTimeUTCOffset = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[3])
            SpecimenCollector = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[0])

            aff = self.get_affiliations_dictionary()
            for m_code,c_time,c_offset,person in zip(CollectionMethodCode,
                                                     CollectionDateTime,
                                                     CollectionDateTimeUTCOffset,
                                                     SpecimenCollector):
                mObj = model.Method()
                mObj.MethodCode = m_code
                aObj = model.Action()
                aObj.Method = mObj
                aObj.ActionTypeCV = "Specimen collection"
                aObj.BeginDateTime = c_time
                aObj.BeginDateTimeUTCOffset = c_offset
                affObj = aff.get(person)
                abObj = model.ActionBy()
                abObj.IsActionLead = True
                abObj.Action = aObj
                abObj.Affiliation = affObj
                aResults.append(abObj)
        return aResults

    def get_all_featureactions(self):

        faResults = []
        scf_list = self.get_all_specimencolumnfinder()
        if scf_list is not None:
            #sampling features
            sp_codes = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[7])
            sp_desc = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[8])
            sp_name = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[9])
            sp_uuid = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[10])

            #action from specimen collection
            CollectionMethodCode = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[1])
            CollectionDateTime = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[2])
            CollectionDateTimeUTCOffset = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[3])

            #actions from specimen analysis
            dc_list = self.get_all_datacolumns()
            AnalysisDateTime = None
            AnalysisDateTimeUTCOffset = None
            AnalysisMethodObj = None
            AnalysisMethodCode = None

            if dc_list is not None:
                for dc in dc_list:
                    ColumnType = getattr(dc,'ColumnType')
                    if ColumnType == 'AnalysisDateTime':
                        adt_col = getattr(dc,'ColumnNumber')
                        AnalysisDateTime = self.get_datavalues_by_column(adt_col)
                        atc_value = getattr(dc,'AppliesToColumn')
                        for x in dc_list:
                            col_label = getattr(x,'ColumnLabel')
                            if col_label == atc_value:
                                AnalysisMethodCode = getattr(x,'AnalysisMethodCode')
                                break
                    if ColumnType == 'AnalysisDateTimeUTCOffset':
                        adto_col = getattr(dc,'ColumnNumber')
                        AnalysisDateTimeUTCOffset = self.get_datavalues_by_column(adto_col)
                AnalysisMethodObj = model.Method()
                AnalysisMethodObj.MethodCode = AnalysisMethodCode

            for sf_code, m_code,c_time,c_offset,a_time,a_offset in zip(sp_codes,
                                                       CollectionMethodCode,
                                                       CollectionDateTime,
                                                       CollectionDateTimeUTCOffset,
                                                       AnalysisDateTime,
                                                       AnalysisDateTimeUTCOffset):
                sf_list = [sp_uuid,None,None,sf_code,sp_name,sp_desc,None,None,None]
                sfObj = model.SamplingFeature()
                sfObj.SamplingFeatureUUID = sp_uuid
                sfObj.SamplingFeatureCode = str(sf_code)
                sfObj.SamplingFeatureName = sp_name
                sfObj.SamplingFeatureDescription = sp_desc

                mObj = model.Method()
                mObj.MethodCode = m_code
                caObj = model.Action()
                caObj.Method = mObj
                caObj.ActionTypeCV = "Specimen collection"
                caObj.BeginDateTime = c_time
                caObj.BeginDateTimeUTCOffset = c_offset
                aaObj = model.Action()
                aaObj.Method = AnalysisMethodObj
                aaObj.ActionTypeCV = "Specimen analysis"
                aaObj.BeginDateTime = a_time
                aaObj.BeginDateTimeUTCOffset = a_offset
                cfaObj = model.FeatureAction()
                cfaObj.SamplingFeature = sfObj
                cfaObj.Action = caObj
                afaObj = model.FeatureAction()
                afaObj.SamplingFeature = sfObj
                afaObj.Action = aaObj
                faResults.append(cfaObj)
                faResults.append(afaObj)

        return faResults

    def get_all_results(self):
        dc_list = self.get_all_datacolumns()
        if dc_list is not None:
            cdt = None
            cdto = None
            cmc = None
            sc = None
            plc = None
            atc = None
            resultvalues = []
            for dc in dc_list:
                ColumnType = getattr(dc,'ColumnType')
                #action
                if ColumnType == 'CollectionDateTime':
                    col = getattr(dc,'ColumnNumber')
                    cdt = self.get_datavalues_by_column(col)
                if ColumnType == 'CollectionDateTimeUTCOffset':
                    col = getattr(dc,'ColumnNumber')
                    cdto = self.get_datavalues_by_column(col)
                if ColumnType == 'CollectionMethodCode':
                    col = getattr(dc,'ColumnNumber')
                    cmc = self.get_datavalues_by_column(col)
                #samplingfeature
                if ColumnType == 'SpecimenCode':
                    col = getattr(dc,'ColumnNumber')
                    sc = self.get_datavalues_by_column(col)
                if ColumnType == 'ProcessingLevelCode':
                    col = getattr(dc,'ColumnNumber')
                    plc = self.get_datavalues_by_column(col)
                    atc = getattr(dc,'AppliesToColumn')

                if ColumnType == 'ResultValue':
                    #col = getattr(dc,'ColumnNumber')
                    #r_values = self.get_datavalues_by_column(col)
                    label = getattr(dc,'ColumnLabel')
                    rtcv = getattr(dc,'ResultTypeCV')
                    vcode = getattr(dc,'VariableCode')
                    uname = getattr(dc,'UnitName')
                    smcv = getattr(dc,'SampledMediumCV')
                    plc = getattr(dc,'ProcessingLevelCode')
                    tcn = getattr(dc,'TaxonomicClassifierName')
                    rv = [label,rtcv,vcode,uname,smcv,plc,tcn]
                    resultvalues.append(rv)
            rResults = []
            for rv in resultvalues:
                if atc == rv[0]:
                    vObj = model.Variable()
                    vObj.VariableCode = rv[2]
                    for c_time,c_offset,c_m_code,sf_code,p_code in zip(cdt,cdto,cmc,sc,plc):
                        sfObj = model.SamplingFeature()
                        sfObj.SamplingFeatureCode = str(sf_code)
                        mObj = model.Method()
                        mObj.MethodCode = c_m_code
                        caObj = model.Action()
                        caObj.BeginDateTime = c_time
                        caObj.BeginDateTimeUTCOffset = c_offset
                        caObj.Method = mObj
                        faObj = model.FeatureAction()
                        faObj.Action = caObj
                        faObj.SamplingFeature = sfObj
                        pObj = model.ProcessingLevel()
                        if isinstance(p_code,float):
                            pObj.ProcessingLevelCode = str(int(p_code))
                        else:
                            pObj.ProcessingLevelCode = p_code
                        rObj = model.Result()
                        rObj.ResultTypeCV = rv[1]
                        rObj.Unit = rv[3]
                        rObj.ResultDateTime = c_time
                        rObj.ResultDateTimeUTCOffset = c_offset
                        rObj.SampledMediumCV = rv[4]
                        rObj.ValueCount = 1
                        rObj.FeatureAction = faObj
                        rObj.Variable = vObj
                        rObj.ProcessingLevel = pObj
                        rObj.TaxonomicClassifier = rv[6]
                        rResults.append(rObj)
                else:
                    vObj = model.Variable()
                    vObj.VariableCode = rv[2]
                    pObj = model.ProcessingLevel()
                    if isinstance(p_code,float):
                        pObj.ProcessingLevelCode = str(int(rv[5]))
                    else:
                        pObj.ProcessingLevelCode = rv[5]
                    for c_time,c_offset,c_m_code,sf_code in zip(cdt,cdto,cmc,sc):
                        sfObj = model.SamplingFeature()
                        sfObj.SamplingFeatureCode = str(sf_code)
                        mObj = model.Method()
                        mObj.MethodCode = c_m_code
                        caObj = model.Action()
                        caObj.BeginDateTime = c_time
                        caObj.BeginDateTimeUTCOffset = c_offset
                        caObj.Method = mObj
                        faObj = model.FeatureAction()
                        faObj.Action = caObj
                        faObj.SamplingFeature = sfObj
                        rObj = model.Result()
                        rObj.ResultTypeCV = rv[1]
                        rObj.Unit = rv[3]
                        rObj.ResultDateTime = c_time
                        rObj.ResultDateTimeUTCOffset = c_offset
                        rObj.SampledMediumCV = rv[4]
                        rObj.ValueCount = 1
                        rObj.FeatureAction = faObj
                        rObj.Variable = vObj
                        rObj.ProcessingLevel = pObj
                        rObj.TaxonomicClassifier = rv[6]
                        rResults.append(rObj)
            return rResults
        else:
            return None

    def get_all_measurementresults(self):
        dc_list = self.get_all_datacolumns()
        if dc_list is not None:
            cdt = None
            cdto = None
            cmc = None
            sc = None
            plc = None
            atc = None
            resultvalues = []
            for dc in dc_list:
                ColumnType = getattr(dc,'ColumnType')
                #action
                if ColumnType == 'CollectionDateTime':
                    col = getattr(dc,'ColumnNumber')
                    cdt = self.get_datavalues_by_column(col)
                if ColumnType == 'CollectionDateTimeUTCOffset':
                    col = getattr(dc,'ColumnNumber')
                    cdto = self.get_datavalues_by_column(col)
                if ColumnType == 'CollectionMethodCode':
                    col = getattr(dc,'ColumnNumber')
                    cmc = self.get_datavalues_by_column(col)
                #samplingfeature
                if ColumnType == 'SpecimenCode':
                    col = getattr(dc,'ColumnNumber')
                    sc = self.get_datavalues_by_column(col)
                if ColumnType == 'ProcessingLevelCode':
                    col = getattr(dc,'ColumnNumber')
                    plc = self.get_datavalues_by_column(col)
                    atc = getattr(dc,'AppliesToColumn')

                if ColumnType == 'ResultValue':
                    #col = getattr(dc,'ColumnNumber')
                    #r_values = self.get_datavalues_by_column(col)
                    label = getattr(dc,'ColumnLabel')
                    rtcv = getattr(dc,'ResultTypeCV')
                    vcode = getattr(dc,'VariableCode')
                    uname = getattr(dc,'UnitName')
                    smcv = getattr(dc,'SampledMediumCV')
                    plc = getattr(dc,'ProcessingLevelCode')
                    tcn = getattr(dc,'TaxonomicClassifierName')
                    cc = getattr(dc,'CensorCodeCV')
                    qc = getattr(dc,'QualityCodeCV')
                    tai = getattr(dc,'TimeAggregationInterval')
                    taiu = getattr(dc,'TimeAggregationIntervalUnitCode')
                    asc = getattr(dc,'AggregationStatisticCV')
                    rv = [label,rtcv,vcode,uname,smcv,plc,tcn,cc,qc,tai,taiu,asc]
                    resultvalues.append(rv)
            rmResults = []
            for rv in resultvalues:
                if atc == rv[0]:
                    vObj = model.Variable()
                    vObj.VariableCode = rv[2]
                    for c_time,c_offset,c_m_code,sf_code,p_code in zip(cdt,cdto,cmc,sc,plc):
                        sfObj = model.SamplingFeature()
                        sfObj.SamplingFeatureCode = str(sf_code)
                        mObj = model.Method()
                        mObj.MethodCode = c_m_code
                        caObj = model.Action()
                        caObj.BeginDateTime = c_time
                        caObj.BeginDateTimeUTCOffset = c_offset
                        caObj.Method = mObj
                        faObj = model.FeatureAction()
                        faObj.Action = caObj
                        faObj.SamplingFeature = sfObj
                        pObj = model.ProcessingLevel()
                        if isinstance(p_code,float):
                            pObj.ProcessingLevelCode = str(int(p_code))
                        else:
                            pObj.ProcessingLevelCode = p_code
                        rObj = model.Result()
                        rObj.ResultTypeCV = rv[1]
                        rObj.Unit = rv[3]
                        rObj.ResultDateTime = c_time
                        rObj.ResultDateTimeUTCOffset = c_offset
                        rObj.SampledMediumCV = rv[4]
                        rObj.ValueCount = 1
                        rObj.FeatureAction = faObj
                        rObj.Variable = vObj
                        rObj.ProcessingLevel = pObj
                        rObj.TaxonomicClassifier = rv[6]
                        rmObj = model.MeasurementResult()
                        rmObj.Result = rObj
                        rmObj.CensorCodeCV = rv[7]
                        rmObj.QualityCodeCV = rv[8]
                        rmObj.TimeAggregationInterval = rv[9]
                        rmObj.TimeAggregationIntervalUnitsID = rv[10]
                        rmObj.AggregationStatisticCV = rv[11]
                        rmResults.append(rmObj)
                else:
                    vObj = model.Variable()
                    vObj.VariableCode = rv[2]
                    pObj = model.ProcessingLevel()
                    if isinstance(rv[5],float):
                        pObj.ProcessingLevelCode = str(int(rv[5]))
                    else:
                        pObj.ProcessingLevelCode = rv[5]
                    for c_time,c_offset,c_m_code,sf_code in zip(cdt,cdto,cmc,sc):
                        sfObj = model.SamplingFeature()
                        sfObj.SamplingFeatureCode = str(sf_code)
                        mObj = model.Method()
                        mObj.MethodCode = c_m_code
                        caObj = model.Action()
                        caObj.BeginDateTime = c_time
                        caObj.BeginDateTimeUTCOffset = c_offset
                        caObj.Method = mObj
                        faObj = model.FeatureAction()
                        faObj.Action = caObj
                        faObj.SamplingFeature = sfObj
                        rObj = model.Result()
                        rObj.ResultTypeCV = rv[1]
                        rObj.Unit = rv[3]
                        rObj.ResultDateTime = c_time
                        rObj.ResultDateTimeUTCOffset = c_offset
                        rObj.SampledMediumCV = rv[4]
                        rObj.ValueCount = 1
                        rObj.FeatureAction = faObj
                        rObj.Variable = vObj
                        rObj.ProcessingLevel = pObj
                        rObj.TaxonomicClassifier = rv[6]
                        rmObj = model.MeasurementResult()
                        rmObj.Result = rObj
                        rmObj.CensorCodeCV = rv[7]
                        rmObj.QualityCodeCV = rv[8]
                        rmObj.TimeAggregationInterval = rv[9]
                        rmObj.TimeAggregationIntervalUnitsID = rv[10]
                        rmObj.AggregationStatisticCV = rv[11]
                        rmResults.append(rmObj)
            return rmResults
        else:
            return None

    def get_all_measurementresultvalues(self):
        dc_list = self.get_all_datacolumns()
        if dc_list is not None:
            cdt = None
            cdto = None
            cmc = None
            sc = None
            plc = None
            atc = None
            resultvalues = []
            for dc in dc_list:
                ColumnType = getattr(dc,'ColumnType')
                #action
                if ColumnType == 'CollectionDateTime':
                    col = getattr(dc,'ColumnNumber')
                    cdt = self.get_datavalues_by_column(col)
                if ColumnType == 'CollectionDateTimeUTCOffset':
                    col = getattr(dc,'ColumnNumber')
                    cdto = self.get_datavalues_by_column(col)
                if ColumnType == 'CollectionMethodCode':
                    col = getattr(dc,'ColumnNumber')
                    cmc = self.get_datavalues_by_column(col)
                #samplingfeature
                if ColumnType == 'SpecimenCode':
                    col = getattr(dc,'ColumnNumber')
                    sc = self.get_datavalues_by_column(col)
                if ColumnType == 'ProcessingLevelCode':
                    col = getattr(dc,'ColumnNumber')
                    plc = self.get_datavalues_by_column(col)
                    atc = getattr(dc,'AppliesToColumn')

                if ColumnType == 'ResultValue':
                    col = getattr(dc,'ColumnNumber')
                    rvalues = self.get_datavalues_by_column(col)
                    label = getattr(dc,'ColumnLabel')
                    rtcv = getattr(dc,'ResultTypeCV')
                    vcode = getattr(dc,'VariableCode')
                    uname = getattr(dc,'UnitName')
                    smcv = getattr(dc,'SampledMediumCV')
                    plc = getattr(dc,'ProcessingLevelCode')
                    tcn = getattr(dc,'TaxonomicClassifierName')
                    cc = getattr(dc,'CensorCodeCV')
                    qc = getattr(dc,'QualityCodeCV')
                    tai = getattr(dc,'TimeAggregationInterval')
                    taiu = getattr(dc,'TimeAggregationIntervalUnitCode')
                    asc = getattr(dc,'AggregationStatisticCV')
                    rv = [label,rtcv,vcode,uname,smcv,plc,tcn,cc,qc,tai,taiu,asc,rvalues]
                    resultvalues.append(rv)
            rmvResults = []
            for rv in resultvalues:
                if atc == rv[0]:
                    vObj = model.Variable()
                    vObj.VariableCode = rv[2]
                    for c_time,c_offset,c_m_code,sf_code,p_code,rvalue in zip(cdt,cdto,cmc,sc,plc,rv[12]):
                        if rvalue is None:
                            continue
                        sfObj = model.SamplingFeature()
                        sfObj.SamplingFeatureCode = str(sf_code)
                        mObj = model.Method()
                        mObj.MethodCode = c_m_code
                        caObj = model.Action()
                        caObj.BeginDateTime = c_time
                        caObj.BeginDateTimeUTCOffset = c_offset
                        caObj.Method = mObj
                        faObj = model.FeatureAction()
                        faObj.Action = caObj
                        faObj.SamplingFeature = sfObj
                        pObj = model.ProcessingLevel()
                        if isinstance(p_code,float):
                            pObj.ProcessingLevelCode = str(int(p_code))
                        else:
                            pObj.ProcessingLevelCode = p_code
                        rObj = model.Result()
                        rObj.ResultTypeCV = rv[1]
                        rObj.Unit = rv[3]
                        rObj.ResultDateTime = c_time
                        rObj.ResultDateTimeUTCOffset = c_offset
                        rObj.SampledMediumCV = rv[4]
                        rObj.ValueCount = 1
                        rObj.FeatureAction = faObj
                        rObj.Variable = vObj
                        rObj.ProcessingLevel = pObj
                        rObj.TaxonomicClassifier = rv[6]
                        rmObj = model.MeasurementResult()
                        rmObj.Result = rObj
                        rmObj.CensorCodeCV = rv[7]
                        rmObj.QualityCodeCV = rv[8]
                        rmObj.TimeAggregationInterval = rv[9]
                        rmObj.TimeAggregationIntervalUnitsID = rv[10]
                        rmObj.AggregationStatisticCV = rv[11]
                        rmvResults.append(model.MeasurementResultValue([rvalue,c_time,c_offset,rmObj]))
                else:
                    vObj = model.Variable()
                    vObj.VariableCode = rv[2]
                    pObj = model.ProcessingLevel()
                    if isinstance(rv[5],float):
                        pObj.ProcessingLevelCode = str(int(rv[5]))
                    else:
                        pObj.ProcessingLevelCode = rv[5]
                    for c_time,c_offset,c_m_code,sf_code,rvalue in zip(cdt,cdto,cmc,sc,rv[12]):
                        if rvalue is None:
                            continue
                        sfObj = model.SamplingFeature()
                        sfObj.SamplingFeatureCode = str(sf_code)
                        mObj = model.Method()
                        mObj.MethodCode = c_m_code
                        caObj = model.Action()
                        caObj.BeginDateTime = c_time
                        caObj.BeginDateTimeUTCOffset = c_offset
                        caObj.Method = mObj
                        faObj = model.FeatureAction()
                        faObj.Action = caObj
                        faObj.SamplingFeature = sfObj
                        rObj = model.Result()
                        rObj.ResultTypeCV = rv[1]
                        rObj.Unit = rv[3]
                        rObj.ResultDateTime = c_time
                        rObj.ResultDateTimeUTCOffset = c_offset
                        rObj.SampledMediumCV = rv[4]
                        rObj.ValueCount = 1
                        rObj.FeatureAction = faObj
                        rObj.Variable = vObj
                        rObj.ProcessingLevel = pObj
                        rObj.TaxonomicClassifier = rv[6]
                        rmObj = model.MeasurementResult()
                        rmObj.Result = rObj
                        rmObj.CensorCodeCV = rv[7]
                        rmObj.QualityCodeCV = rv[8]
                        rmObj.TimeAggregationInterval = rv[9]
                        rmObj.TimeAggregationIntervalUnitsID = rv[10]
                        rmObj.AggregationStatisticCV = rv[11]
                        rmvResults.append(model.MeasurementResultValue([rvalue,c_time,c_offset,rmObj]))
            return rmvResults
        else:
            return None

    def get_all_methods(self):
        sheet = xw.Sheet(Sheet_Names["7"])
        if sheet is None:
            return None

        NumMethods = xw.Range(sheet,'NumMethods').value
        if NumMethods is None or NumMethods < 0:
            return None

        Methods = xw.Range(sheet,'Methods').value
        mResults = []
        for m in Methods:
            if any(m):
                if m[5] is not None: #Organization
                    org_obj = model.Organization()
                    org_obj.OrganizationName = m[5]
                    m.insert(5,org_obj)
                mResults.append(model.Method(m))
        return mResults

    def get_all_variables(self):
        sheet = xw.Sheet('Variables')
        if sheet is None:
            return None

        NumVariables = xw.Range(sheet,'NumVariables').value
        if NumVariables is None or NumVariables < 0:
            return None

        Variables = xw.Range(sheet,'Variables').value
        vResults = []
        for v in Variables:
            if any(v):
                vResults.append(model.Variable(v))
        return vResults

    def get_all_processinglevels(self):
        sheet = xw.Sheet('Processing Levels')
        if sheet is None:
            return None

        NumProcessingLevels = xw.Range(sheet,'NumProcessingLevels').value
        if NumProcessingLevels is None or NumProcessingLevels < 0:
            return None

        plResults = []
        ProcessingLevels = xw.Range(sheet,'ProcessingLevels').value
        for p in ProcessingLevels:
            if any(p):
                plResults.append(model.ProcessingLevel(p))
        return plResults

    def get_all_datacolumns(self):
        sheet = xw.Sheet(Sheet_Names["11"])
        if sheet is None:
            return None

        NumFileColumns = xw.Range(sheet,'NumFileColumns').value
        SpecimenColumnNumber = xw.Range(sheet,'SpecimenColumnNumber').value
        NumSpecimens = xw.Range(sheet,'NumSpecimens').value
        NumDataColumns = xw.Range(sheet,'NumDataColumns').value

        if (NumDataColumns is None and NumDataColumns == 0) and \
            (NumSpecimens is None and NumSpecimens == 0):
            return None
        datacloumnResults = []
        DataColumns = xw.Range(sheet,'DataColumns').value
        for d in DataColumns:
            if any(d):
                #d.append(NumFileColumns)
                #d.append(SpecimenColumnNumber)
                #d.append(NumSpecimens)
                #d.append(NumDataColumns)
                datacloumnResults.append(model.DataColumn(d))
        return datacloumnResults

    def get_all_datavalues(self):
        sheet = xw.Sheet(Sheet_Names["12"])
        if sheet is None:
            return None
        DataValues = xw.Range(sheet,'A1').table.value
        dvheader = DataValues[0]
        datavalueResults = []
        for dv in DataValues[1:]:
            dvobj = model.DataValue(dvheader,dv)
            datavalueResults.append(dvobj)
        return datavalueResults

    def get_datavalues_by_column(self,col):
        sheet = xw.Sheet(Sheet_Names["12"])
        if sheet is None:
            return None

        sheet1 = xw.Sheet(Sheet_Names["11"])
        if sheet is None:
            return None

        NumSpecimens = xw.Range(sheet1,'NumSpecimens').value
        DataValues = xw.Range(sheet,(2,int(col)),(int(NumSpecimens)+1,int(col))).value
        return DataValues

    def get_all_spatialreferences(self):
        sheet = xw.Sheet(Sheet_Names["21"])
        if sheet is None:
            return None
        sr = xw.Range(sheet,'SpatialReferences').value
        srResults = []
        for s in sr:
            if any(s):
                srResults.append(model.SpatialReference(s))
        return srResults

    def get_all_child_samplingfeatures(self):
        scf_list = self.get_all_specimencolumnfinder()
        if scf_list is None:
            return None

        sp_codes = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[7])
        sp_desc = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[8])
        sp_name = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[9])
        sp_uuid = self.get_datavalue_from_finder('specimen',scf_list,Column_Names[0],DataType_Names[10])

        c_sfResults = []
        for code in sp_codes:
            sfObj = model.SamplingFeature()
            sfObj.SamplingFeatureUUID = sp_uuid
            sfObj.SamplingFeatureCode = str(code)
            sfObj.SamplingFeatureName = sp_name
            sfObj.SamplingFeatureDescription = sp_desc
            c_sfResults.append(sfObj)
        return c_sfResults

    def get_datavalue_from_finder(self,finder_type,scf,col_name,dt_name):
        item = None
        for x in scf:
            DataType = x.__getattribute__(col_name)
            if DataType == dt_name:
                item = x
                break

        FirstValueAddress = item.__getattribute__(Column_Names[1])
        if FirstValueAddress_Names[0] in FirstValueAddress:
            DataValuesColumnNumber = item.__getattribute__(Column_Names[2])
            spResults = self.get_datavalues_by_column(int(DataValuesColumnNumber))
            return spResults
        elif FirstValueAddress_Names[1] in FirstValueAddress:
            #DataColumnsInputColumn = sp_item.__getattribute__(Column_Names[3])
            #print "DataColumnsInputColumn: %s" % DataColumnsInputColumn
            dcResults = self.get_all_datacolumns()
            if dcResults is not None and len(dcResults) > 0:
                for dc in dcResults:
                    if finder_type == 'specimen':
                        dc_value = dc.__getattribute__(dt_name)
                        if dc_value is not None:
                            return dc_value
                    elif finder_type == 'result':
                        DVNum = item.__getattribute__(Column_Names[4])
                        dc_dvnum_value = dc.__getattribute__('DVNum')
                        if DVNum == dc_dvnum_value:
                            dc_value = dc.__getattribute__(dt_name)
                            if dc_value is not None:
                                return dc_value
            return None
        elif FirstValueAddress_Names[2] in FirstValueAddress:
            return None
        else:
            return None

    def get_all_specimencolumnfinder(self):
        sheet = xw.Sheet(Sheet_Names["13"])
        first_row = xw.Range(sheet,'SpecimenColumnFinder').row
        first_col = xw.Range(sheet,'SpecimenColumnFinder').column
        last_row = xw.Range(sheet,'SpecimenColumnFinder').last_cell.row
        last_col = xw.Range(sheet,'SpecimenColumnFinder').last_cell.column

        scf_header = xw.Range(sheet,(first_row-1,first_col),
                              (first_row-1,last_col)).horizontal.value
        for scf_title in scf_header:
            if not scf_title in Specimen_Comlun_Finder:
                return None
        scfResults = []
        for x in range(first_row,last_row+1): #row
            scf_list = []
            for y in range(first_col,last_col+1): #column
                cell = xw.Range(sheet,(x,y)).value
                scf_list.append(cell)
            scf_obj = model.SpecimenColumnFinder(scf_list)
            if not isinstance(scf_obj.DataValuesColumnNumber, float):
                scf_obj.DataValuesColumnNumber = 0.0
            if not isinstance(scf_obj.DataColumnsInputColumn, float):
                scf_obj.DataColumnsInputColumn = 0.0
            scfResults.append(scf_obj)
        return scfResults

    def get_all_resultcolumnfinder(self):
        sheet = xw.Sheet(Sheet_Names["15"])
        first_row = xw.Range(sheet,'ResultColumnFinder').row
        first_col = xw.Range(sheet,'ResultColumnFinder').column
        last_row = xw.Range(sheet,'ResultColumnFinder').last_cell.row
        last_col = xw.Range(sheet,'ResultColumnFinder').last_cell.column

        rcf_header = xw.Range(sheet,(first_row-1,first_col),
                              (first_row-1,last_col)).horizontal.value
        for rcf_title in rcf_header:
            if not rcf_title in Result_Column_Finder:
                return None
        rcfResults = []
        for x in range(first_row,last_row+1): #row
            rcf_list = []
            for y in range(first_col,last_col+1): #column
                cell = xw.Range(sheet,(x,y)).value
                rcf_list.append(cell)
            rcf_obj = model.ResultColumnFinder(rcf_list)
            if not isinstance(rcf_obj.DataValuesColumnNumber, float):
                rcf_obj.DataValuesColumnNumber = 0.0
            if not isinstance(rcf_obj.DataColumnsInputColumn, float):
                rcf_obj.DataColumnsInputColumn = 0.0
            rcfResults.append(rcf_obj)
        return rcfResults
