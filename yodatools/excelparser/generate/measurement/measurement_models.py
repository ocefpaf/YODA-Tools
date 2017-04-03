#import sys
#sys.path.append("..")

import yodatools.excelparser.YODAPy.ydt.models as ydt_base

class YODAHeader(ydt_base.BaseYODAHeader):
    def __init__(self, yh=None):
        if isinstance(yh,list):
            self.YODAVersion = yh[0]
            self.TemplateProfile = yh[1]
            self.TemplateVersion = yh[2]
            self.VocabUpdate = yh[3]

class Person(ydt_base.BasePerson):
    def __init__(self, p=None):
        if isinstance(p,list):
            self.PersonFirstName = p[0]
            self.PersonMiddleName = p[1]
            self.PersonLastName = p[2]

class Affiliation(ydt_base.BaseAffiliation):
    def __init__(self, a=None):
        if isinstance(a,list):
            self.PrimaryEmail = a[0] #a[4]
            self.PrimaryAddress = a[1] #a[5]
            #self.PrimaryPhone = None
            #self.IsPrimaryOrganizationContact = None
            #self.AffiliationStartDate = None
            #self.AffiliationEndDate = None
            #self.PersonLink = None

            self.Person = a[2]
            self.Organization = a[3] #

class PersonExternalIdentifier(ydt_base.BasePersonExternalIdentifier):
    def __init__(self,pe=None):
        self.PersonExternalIdentifier = pe[0]
        self.PersonExternalIdentifierURI = pe[1]

        self.Person = pe[2]
        self.ExternalIdentifierSystem = pe[3]

class Organization(ydt_base.BaseOrganization):
    def __init__(self, org=None):
        if isinstance(org,list):
            self.OrganizationTypeCV = org[0]
            self.OrganizationCode = org[1]
            self.OrganizationName = org[2]
            self.OrganizationDescription = org[3]
            self.OrganizationLink = org[4]

class Dataset(ydt_base.BasedDataset):
    def __init__(self, ds=None):
        if isinstance(ds,list):
            self.DataSetUUID = ds[0]
            self.DataSetTypeCV = ds[1]
            self.DataSetCode = ds[2]
            self.DataSetTitle = ds[3]
            self.DataSetAbstract = ds[4]

class Citation(ydt_base.BaseCitation):
    def __init__(self, ec=None):
        if isinstance(ec,list):
            self.Title = ec[0]
            self.Publisher = ec[1]
            self.PublicationYear = ec[2]
            self.CitationLink = ec[3]

class DataSetCitation(ydt_base.BaseDataSetCitation):
    def __init__(self, dc=None):
        if isinstance(dc,list):
            self.RelationshipTypeCV = dc[0]
            self.DataSet = dc[1]
            self.Citation = dc[2]

class AuthorList(ydt_base.BaseAuthorList):
    yaml_tag = u'!AuthorList'
    def __init__(self,author):
        if isinstance(author,list):
            self.AuthorOrder = author[0]
            self.Citation = author[1]
            self.Person = author[2]

class SamplingFeature(ydt_base.BaseSamplingFeature):
    def __init__(self, sf=None):
        if isinstance(sf,list):
            self.SamplingFeatureUUID = sf[0]
            self.SamplingFeatureTypeCV = sf[1]
            self.SamplingFeatureGeotypeCV = sf[2]
            self.SamplingFeatureCode = sf[3]
            self.SamplingFeatureName = sf[4]
            self.SamplingFeatureDescription = sf[5]
            self.FeatureGeometry = sf[6]
            self.Elevation_m = sf[7]
            self.ElevationDatumCV = sf[8]

class Site(ydt_base.BaseSite):
    def __init__(self,s=None):
        if isinstance(s,list):
            self.SiteTypeCV = s[0]
            self.Latitude = s[1]
            self.Longitude = s[2]
            self.SamplingFeature = s[3]
            self.SpatialReference = s[4]

class Specimen(ydt_base.BaseSpecimen):
    def __init__(self,sp=None):
        if isinstance(sp,list):
            self.SpecimenTypeCV = sp[0]
            self.SpecimenMediumCV = sp[1]
            self.IsFieldSpecimen = sp[2]
            self.SamplingFeature = sp[3]

class SpatialOffset(ydt_base.BaseSpatialOffset):
    def __init__(self, so=None):
        if isinstance(so,list):
            self.SpatialOffsetCode = so[0]
            self.SpatialOffsetTypeCV = so[1]
            self.Offset1Value = so[2]
            self.Offset1Unit = so[3]
            self.Offset2Value = so[4]
            self.Offset2Unit = so[5]
            self.Offset3Value = so[6]
            self.Offset3Unit = so[7]

class RelatedFeature(ydt_base.BaseRelatedFeature):
    def __init__(self, rf=None):
        if isinstance(rf,list):
            self.RelationshipTypeCV = rf[0]
            self.SamplingFeature = rf[1]
            self.RelatedFeature = rf[2]
            self.SpatialOffset = rf[3]

class Method(ydt_base.BaseMethod):
    def __init__(self, m=None):
        if isinstance(m,list):
            self.MethodTypeCV = m[0]
            self.MethodCode = m[1]
            self.MethodName = m[2]
            self.MethodDescription = m[3]
            self.MethodLink = m[4]
            self.Organization = m[5]

class Action(ydt_base.BaseAction):
    def __init__(self, a=None):
        if isinstance(a,list):
            self.ActionTypeCV = a[0]
            self.BeginDateTime = a[1]
            self.BeginDateTimeUTCOffset = a[2]
            self.EndDateTime = a[3]
            self.EndDateTimeUTCOffset = a[4]
            self.ActionDescription = a[5]
            self.ActionFileLink = a[6]
            self.Method = a[7]

class ActionBy(ydt_base.BaseActionBy):
    def __init__(self, ab=None):
        if isinstance(ab,list):
            self.IsActionLead = ab[0]
            self.RoleDescription = ab[1]
            self.Action = ab[2]
            self.Affiliation = ab[3]

class Variable(ydt_base.BaseVariable):
    def __init__(self, v=None):
        if isinstance(v,list):
            self.VariableTypeCV = v[0]
            self.VariableCode = v[1]
            self.VariableNameCV = v[2]
            self.VariableDefinition = v[3]
            self.SpeciationCV = v[4]
            self.NoDataValue = v[5]

class ProcessingLevel(ydt_base.BaseProcessingLevel):
    def __init__(self,pl=None):
        if isinstance(pl,list):
            if isinstance(pl[0],float):
                self.ProcessingLevelCode = str(int(pl[0]))
            else:
                self.ProcessingLevelCode = pl[0]
            self.Definition = pl[1]
            self.Explanation = pl[2]

class FeatureAction(ydt_base.BaseFeatureAction):
    def __init__(self,fa=None):
        if isinstance(fa,list):
            self.SamplingFeature = fa[0]
            self.Action = fa[1]

class Result(ydt_base.BaseResult):
    def __init__(self,r=None):
        if isinstance(r,list):
            self.ResultUUID = r[0]
            self.ResultTypeCV = r[1]
            self.Unit = r[2]
            self.ResultDateTime = r[3]
            self.ResultDateTimeUTCOffset = r[4]
            self.ValidDateTime = r[5]
            self.ValidDateTimeUTCOffset = r[6]
            self.StatusCV = r[7]
            self.SampledMediumCV = r[8]
            self.ValueCount = r[9]

            self.FeatureAction = r[10]
            self.Variable = r[11]
            self.ProcessingLevel = r[12]
            self.TaxonomicClassifier = r[13]

class MeasurementResult(ydt_base.BaseMeasurementResult):
    def __init__(self, mr=None):
        if isinstance(mr,list):
            self.XLocation = mr[0]
            self.XLocationUnitsID = mr[1]
            self.YLocation = mr[2]
            self.YLocationUnitsID = mr[3]
            self.ZLocation = mr[4]
            self.ZLocationUnitsID = mr[5]
            self.CensorCodeCV = mr[6]
            self.QualityCodeCV = mr[7]
            self.AggregationStatisticCV = mr[8]
            self.TimeAggregationInterval = mr[9]
            self.TimeAggregationIntervalUnitsID = mr[10]

            self.Result = mr[11]
            self.SpatialReference = mr[12]

class MeasurementResultValue(ydt_base.BaseMeasurementResultValue):
    def __init__(self,mrv=None):
        if isinstance(mrv,list):
            self.DataValue = mrv[0]
            self.ValueDateTime = mrv[1]
            self.ValueDateTimeUTCOffset = mrv[2]
            self.MeasurementResult = mrv[3]

class DataColumn(ydt_base.BaseDataColumn):
    def __init__(self, dc=None):
        if isinstance(dc,list):
            self.ColumnNumber = dc[0]
            self.ColumnLabel = dc[1]
            self.ColumnType = dc[2]
            self.AppliesToColumn = dc[3]
            self.ParentSamplingFeatureCode = dc[4]
            self.RelationshipTypeCV = dc[5]
            self.CollectionDateTimeUTCOffset = dc[6]
            self.SpecimenCollector = dc[7]
            self.CollectionMethodCode = dc[8]
            self.SpecimenMediumCV = dc[9]
            self.SpecimenTypeCV = dc[10]
            self.IsFieldSpecimen = dc[11]
            self.SpatialOffsetCode = dc[12]
            self.ResultTypeCV = dc[13]
            self.VariableCode = dc[14]
            self.UnitName = dc[15]
            self.SampledMediumCV = dc[16]
            self.ResultAnalyst = dc[17]
            self.AnalysisDateTimeUTCOffset = dc[18]
            self.AnalysisMethodCode = dc[19]
            self.ProcessingLevelCode = dc[20]
            self.CensorCodeCV = dc[21]
            self.QualityCodeCV = dc[22]
            self.TaxonomicClassifierName = dc[23]
            self.TimeAggregationInterval = dc[24]
            self.TimeAggregationIntervalUnitCode = dc[25]
            self.AggregationStatisticCV = dc[26]
            self.DVNum = dc[27]
            self.Concat = dc[28]
            #self.NumFileColumns = dc[29]
            #self.SpecimenColumnNumber = dc[30]
            #self.NumSpecimens = dc[31]
            #self.NumDataColumns = dc[32]

class DataValue(ydt_base.BaseDataValue):
    def __init__(self, dvheader=None, dv=None):
        if isinstance(dvheader, list):
            for name, value in zip(dvheader, dv):
                ydt_base.BaseDataValue.__setattr__(self,name,value)

class SpatialReference(ydt_base.BaseSpatialReference):
    def __init__(self, sr=None):
        if isinstance(sr,list):
            self.SRSCode = sr[0]
            self.SRSName = sr[1]
            self.SRSDescription = sr[2]
            self.SRSLink = sr[3]

class ExternalIdentifierSystem(ydt_base.BaseExternalIdentifierSystem):
    def __init__(self, eid=None):
        if isinstance(eid,list):
            self.ExternalIdentifierSystemName = eid[0]
            self.ExternalIdentifierSystemDescrption = eid[1]
            self.ExternalIdentifierSystemURL = eid[2]
            self.URIStructure = eid[3]

            self.IdentifierSystemOrganization = eid[4]

class SpecimenColumnFinder(ydt_base.BaseSpecimenColumnFinder):
    def __init__(self,scf=None):
        if isinstance(scf,list):
            self.DataType = scf[0]
            self.ODMTable = scf[1]
            self.CVName = scf[2]
            self.REQUIRED = scf[3]
            self.VBVorColumn = scf[4]
            self.DataColumnsInputColumn = scf[5]
            self.DataValuesColumnNumber = scf[6]
            self.NumRequired = scf[7]
            self.NumGiven = scf[8]
            self.Error = scf[9]
            self.FirstValueAddress = scf[10]
            self.FirstValue = scf[11]

class ResultColumnFinder(ydt_base.BaseResultColumnFinder):
    def __init__(self, rcf=None):
        if isinstance(rcf,list):
            self.DataType = rcf[0]
            self.ODMTable = rcf[1]
            self.CVName = rcf[2]
            self.REQUIRED = rcf[3]
            self.VBVorColumn = rcf[4]
            self.DVNum = rcf[5]
            self.DataValueLabel = rcf[6]
            self.Concat = rcf[7]
            self.Concat2 = rcf[8]
            self.DataColumnsInputColumn = rcf[9]
            self.DataValuesInputRow = rcf[10]
            self.DataValuesColumnNumber = rcf[11]
            self.NumRequired = rcf[12]
            self.NumGiven = rcf[13]
            self.Error = rcf[14]
            self.FirstValueAddress = rcf[15]
            self.FirstValue = rcf[16]
