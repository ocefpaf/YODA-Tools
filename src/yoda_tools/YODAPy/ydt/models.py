
class BaseYODAHeader(object):
    YODAVersion = None
    TemplateProfile = None
    TemplateVersion = None
    VocabUpdate = None

"""
class BasePeople(object):
    FirstName = None
    MiddleName = None
    LastName = None
    OrganizationName = None
    PrimaryEmail = None
    PrimaryAddress = None
    PersonOrcID = None
    FullName = None
    ExternalIDNum = None
"""

class BaseOrganization(object):
    OrganizationTypeCV = None
    OrganizationCode = None
    OrganizationName = None
    OrganizationDescription = None
    OrganizationLink = None
    ParentOrganizationID = None

class BasePerson(object):
    PersonFirstName = None
    PersonMiddleName = None
    PersonLastName = None

class BaseAffiliation(object):
    IsPrimaryOrganizationContact = None
    AffiliationStartDate = None
    AffiliationEndDate = None
    PrimaryPhone = None
    PrimaryEmail = None
    PrimaryAddress = None
    PersonLink = None

    Person = BasePerson()
    Organization = BaseOrganization()

class BaseExternalIdentifierSystem(object):
    ExternalIdentifierSystemName = None
    ExternalIdentifierSystemDescription = None
    ExternalIdentifierSystemURL = None
    URIStructure = None #in xl sheet, not in odm2 model

    IdentifierSystemOrganization = BaseOrganization()

class BasePersonExternalIdentifier(object):
    PersonExternalIdentifier = None
    PersonExternalIdentifierURI = None

    Person = BasePerson()
    ExternalIdentifierSystem = BaseExternalIdentifierSystem()

class BasedDataset(object):
    DataSetUUID = None
    DataSetTypeCV = None
    DataSetCode = None
    DataSetTitle = None
    DataSetAbstract = None

class BaseCitation(object):
    Title = None
    Publisher = None
    PublicationYear = None
    CitationLink = None

class BaseDataSetCitation(object):
    RelationshipTypeCV = None

    DataSet = BasedDataset()
    Citation = BaseCitation()

class BaseAuthorList(object):
    AuthorOrder = None

    Citation = BaseCitation()
    Person = BasePerson()

class BaseSamplingFeature(object):
    SamplingFeatureUUID = None
    SamplingFeatureTypeCV = None
    SamplingFeatureCode = None
    SamplingFeatureName = None
    SamplingFeatureDescription = None
    SamplingFeatureGeotypeCV = None
    Elevation_m = None
    ElevationDatumCV = None
    FeatureGeometry = None

class BaseSpatialReference(object):
    SRSCode = None
    SRSName = None
    SRSDescription = None
    SRSLink = None

class BaseSite(object):
    SiteTypeCV = None
    Latitude = None
    Longitude = None
    SamplingFeature = BaseSamplingFeature()
    SpatialReference = BaseSpatialReference()

class BaseSpecimen(object):
    SpecimenTypeCV = None
    SpecimenMediumCV = None
    IsFieldSpecimen = None
    SamplingFeature = BaseSamplingFeature()

class BaseSpatialOffset(object):
    SpatialOffsetCode = None # not in ODM2
    SpatialOffsetTypeCV = None
    Offset1Value = None
    Offset1Unit = None
    Offset2Value = None
    Offset2Unit = None
    Offset3Value = None
    Offset3Unit = None

class BaseRelatedFeature(object):

    RelationshipTypeCV = None

    SamplingFeature = BaseSamplingFeature() #"FirstSamplingFeatureCode", child
    RelatedFeature = BaseSamplingFeature() #"SecondSamplingFeatureCode", parent
    SpatialOffset = BaseSpatialOffset() #"SpatialOffsetCode"

class BaseMethod(object):
    MethodTypeCV = None
    MethodCode = None
    MethodName = None
    MethodDescription = None
    MethodLink = None

    Organization = BaseOrganization()

class BaseAction(object):
    ActionTypeCV = None
    BeginDateTime = None
    BeginDateTimeUTCOffset = None
    EndDateTime = None
    EndDateTimeUTCOffset = None
    ActionDescription = None
    ActionFileLink = None

    Method = BaseMethod()

class BaseActionBy(object):
    IsActionLead = None
    RoleDescription = None

    Action = BaseAction()
    Affiliation = BaseAffiliation()

class BaseVariable(object):
    VariableTypeCV = None
    VariableCode = None
    VariableNameCV = None
    VariableDefinition = None
    SpeciationCV = None
    NoDataValue = None

class BaseProcessingLevel(object):
    ProcessingLevelCode = None
    Definition = None
    Explanation = None

class BaseFeatureAction(object):
    SamplingFeature = BaseSamplingFeature()
    Action = BaseAction()

class BaseResult(object):
    ResultUUID = None
    ResultTypeCV = None
    Unit = None
    ResultDateTime = None
    ResultDateTimeUTCOffset = None
    ValidDateTime = None
    ValidDateTimeUTCOffset = None
    StatusCV = None
    SampledMediumCV = None
    ValueCount = None

    FeatureAction = BaseSamplingFeature()
    Variable = BaseVariable()
    ProcessingLevel = BaseProcessingLevel()
    TaxonomicClassifier = None

class BaseMeasurementResult(object):

    XLocation = None
    XLocationUnitsID = None
    YLocation = None
    YLocationUnitsID = None
    ZLocation = None
    ZLocationUnitsID = None
    CensorCodeCV = None
    QualityCodeCV = None
    AggregationStatisticCV = None
    TimeAggregationInterval = None
    TimeAggregationIntervalUnitsID = None

    Result = BaseResult()
    SpatialReference = BaseSpatialReference()

class BaseMeasurementResultValue(object):
    DataValue = None
    ValueDateTime = None
    ValueDateTimeUTCOffset = None

    MeausrementResult = BaseMeasurementResult()

class BaseDataColumn(object):
    ColumnNumber = None
    ColumnLabel = None
    ColumnType = None
    AppliesToColumn = None
    ParentSamplingFeatureCode = None
    RelationshipTypeCV = None
    CollectionDateTimeUTCOffset = None
    SpecimenCollector = None
    CollectionMethodCode = None
    SpecimenMediumCV = None
    SpecimenTypeCV = None
    IsFieldSpecimen = None
    SpatialOffsetCode = None
    ResultTypeCV = None
    VariableCode = None
    UnitName = None
    SampledMediumCV = None
    ResultAnalyst = None
    AnalysisDateTimeUTCOffset = None
    AnalysisMethodCode = None
    ProcessingLevelCode = None
    CensorCodeCV = None
    QualityCodeCV = None
    TaxonomicClassifierName = None
    TimeAggregationInterval = None
    TimeAggregationIntervalUnitCode = None
    AggregationStatisticCV = None
    DVNum = None
    Concat = None
    #NumFileColumns = None
    #SpecimenColumnNumber = None
    #NumSpecimens = None
    #NumDataColumns = None

class BaseDataValue(object):
    # dynamically variables coming from "CoulmnLabel" in BaseDataColumn class
    pass

class BaseSpecimenColumnFinder(object):
    DataType = None
    ODMTable = None
    CVName = None
    REQUIRED = None
    VBVorColumn = None
    DataColumnsInputColumn = None
    DataValuesColumnNumber = None
    NumRequired = None
    NumGiven = None
    Error = None
    FirstValueAddress = None
    FirstValue = None

class BaseResultColumnFinder(object):
    DataType = None
    ODMTable = None
    CVName = None
    REQUIRED = None
    VBVorColumn = None
    DVNum = None
    DataValueLabel = None
    Concat = None
    Concat2 = None
    DataColumnsInputColumn = None
    DataValuesInputRow = None
    DataValuesColumnNumber = None
    NumRequired = None
    NumGiven = None
    Error = None
    FirstValueAddress = None
    FirstValue = None
