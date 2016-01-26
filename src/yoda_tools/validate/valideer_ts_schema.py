import valideer as V
from valideer import String, Integer, ValidationError, Validator, Datetime, Date, Number, Boolean
import datetime

class Datacolummn0(Datetime):

    name = "datacolumn0"

    def __init__(self):
        super(Datacolummn0, self).__init__()

    def validate(self, value, adapt=True):
        if value != None:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        super(Datacolummn0, self).validate(value)
        return value

class DatetimeFormat(Datetime):

    name = "datetime_format"

    def __init__(self):
        super(DatetimeFormat, self).__init__()

    def validate(self, value, adapt=True):
        if value != None:
            value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        super(DatetimeFormat, self).validate(value)
        return value

class DateFormat(Date):

    name = "date_format"

    def __init__(self):
        super(DateFormat, self).__init__()

    def validate(self, value, adapt=True):
        if value != None:
            value = datetime.datetime.strptime(value, "%Y-%m-%d")

        super(DateFormat, self).validate(value)
        return value

class Datacolummn1(Integer):

    name = "datacolumn1"

    def __init__(self):
        super(Datacolummn1, self).__init__()

    def validate(self, value, adapt=True):
        super(Datacolummn1, self).validate(value)

        return value

class Datacolummn2(Number):

    name = "datacolumn2"

    def __init__(self):
        super(Datacolummn2, self).__init__()

    def validate(self, value, adapt=True):
        super(Datacolummn2, self).validate(value)
    
        return value

class To_bool(Boolean):

    name = "tobool"

    def __init__(self):
        super(To_bool, self).__init__()

    def to_bool(self, value):
        valid = {'true': True, 't': True, '1': True,
                 'false': False, 'f': False, '0': False,
        }   
        
        if isinstance(value, bool):
            return value

        if not isinstance(value, basestring):
            raise ValidationError('invalid literal for boolean. Not a string.')

        lower_value = value.lower()
        if lower_value in valid:
            return valid[lower_value]
        else:
            raise ValidationError('invalid literal for boolean: "%s"' % value)


    def validate(self, value, adapt=True):
        super(To_bool, self).validate(self.to_bool(value))
            
        return value


class TimeseriesSchema(object):

    def __init__(self,logger):
        self.logger = logger

    def organization(self):
        org_schema = {
            "OrganizationTypeCV": "string",
            "OrganizationCode": "string",
            "OrganizationName": "string",
            "OrganizationDescription": "?string",
            "OrganizationLink": "?string",
#            "?OrganizationObj": V.Nullable(self.organization()),
        }
        return org_schema

    def method(self):
        method_schema = {
            "MethodTypeCV": "string",
            "MethodCode": "string",
            "MethodName": "string",
            "MethodDescription": "?string",
            "MethodLink": "?string",
            "OrganizationObj": V.Nullable(self.organization()),
        }
        return method_schema

    def action(self):
        action_schema = {
            "ActionTypeCV": "string",
#            "BeginDateTime": "?datetime",
            "BeginDateTime": "datetime_format",
            "BeginDateTimeUTCOffset": "integer",
#            "EndDateTime": "?datetime",
            "EndDateTime": "?datetime_format",
            "EndDateTimeUTCOffset": "?integer",
            "ActionDescription": "?string",
            "ActionFileLink": "?string",
            "MethodObj": self.method(),
        }
        return action_schema

    def samplingfeature(self):

        sf_schema = {
            "SamplingFeatureUUID": "?string",
            "SamplingFeatureTypeCV": "string",
            "SamplingFeatureCode": "string",
            "SamplingFeatureName": "?string",
            "SamplingFeatureDescription": "?string",
            "SamplingFeatureGeotypeCV": "?string",
            "Elevation_m": V.Nullable(V.AdaptTo(float)),
            "ElevationDatumCV": "?string",
            "FeatureGeometry": "?string", #Geometry(?)
        }
        return sf_schema

    def externalidentifiersystem(self):

        eis_schema = {
            "ExternalIdentifierSystemName": "string",
            "ExternalIdentifierSystemDescription": "?string",
            "ExternalIdentifierSystemURL": "?string",
            "IdentifierSystemOrganizationObj": self.organization(),
        }
        return eis_schema

    def sfexternalidentifier(self):

        sfei_schema = {
            "SamplingFeatureObj": self.samplingfeature(),
            "ExternalIdentifierSystemObj": self.externalidentifiersystem(),
            "SamplingFeatureExternalIdentifier": "string",
            "SamplingFeatureExternalIdentifierURI": "?string",
        }
        return sfei_schema

    def variable(self):
        var_schema = {
            "VariableTypeCV": "string",
            "VariableCode": "string",
            "VariableNameCV": "string",
            "VariableDefinition": "?string",
            "SpeciationCV": "?string",
            "NoDataValue": V.Nullable(V.AdaptTo(float)),
        }
        return var_schema

    def processinglevel(self):
        pl_schema = {
            "ProcessingLevelCode": "string",
            "Definition": "?string",
            "Explanation": "?string",
        }
        return pl_schema

    def featureaction(self):
        fa_schema = {
            "SamplingFeatureObj": self.samplingfeature(),
            "ActionObj": self.action(),
        }
        return fa_schema

    def result(self):
        result_schema = {
            "ResultUUID": "?string",
            "ResultTypeCV": "string",
            "ResultDateTime": "?datetime_format",
            "ResultDateTimeUTCOffset": "?integer",
            "ValidDateTime": "?datetime_format",
            "ValidDateTimeUTCOffset": "?integer",
            "StatusCV": "?string",
            "SampledMediumCV": "string",
            "ValueCount": "integer",
            "FeatureActionObj": self.featureaction(),
            "VariableObj": self.variable(),
            "UnitsObj": self.unit(),
            "TaxonomicClassifierObj": V.Nullable(self.taxonimicclassifier()),
            "ProcessingLevelObj": self.processinglevel(),
        }
        return result_schema
    
    def dataset(self):
        ds_schema = {
            "DataSetUUID": "?string",
            "DataSetTypeCV": "string",
            "DataSetCode": "string",
            "DataSetTitle": "string",
            "DataSetAbstract": "string",
        }
        return ds_schema

    def datasetresult(self):
        dsr_schema = {
            "DataSetObj": self.dataset(),
            "ResultObj": self.result(),
        }
        return dsr_schema

    def spatialreference(self):
        sr_schema = {
            "SRSCode": "?string",
            "SRSName": "string",
            "SRSDescription": "?string",
            "SRSLink": "?string",
        }
        return sr_schema

    def site(self):
        site_schema = {
            "SiteTypeCV": "string",
            "Latitude": V.AdaptTo(float),
            "Longitude": V.AdaptTo(float),
            "SamplingFeatureObj": self.samplingfeature(),
            "SpatialReferenceObj": self.spatialreference(),
        }
        return site_schema

    def people(self):
        person_schema = {
            "PersonFirstName": "string",
            "PersonMiddleName": "?string",
            "PersonLastName": "string",
        }
        return person_schema

    def affiliation(self):
        aff_schema = {
            "IsPrimaryOrganizationContact": "?boolean",
            "AffiliationStartDate": "date_format",
            "AffiliationEndDate": "?date_format",
            "PrimaryPhone": "?string",
            "PrimaryEmail": "string",
            "PrimaryAddress": "?string",
            "PersonLink": "?string",
            "PersonObj": self.people(),
            "OrganizationObj": V.Nullable(self.organization()),
        }
        return aff_schema

    def citation(self):
        c_schema = {
            "Title": "string",
            "Publisher": "string",
            "PublicationYear": "string",
            "CitationLink": "?string",
        }
        return c_schema

    def specimen(self):
        specimen_schema = {
            "SpecimenTypeCV": "string",
            "SpecimenMediumCV": "string",
            "IsFieldSpecimen": "tobool", #convert to boolean
            "SamplingFeatureObj": self.samplingfeature(),
        }
        return specimen_schema

    def yoda(self):
        yoda_schema = {
            "Profile": "?string",
            "DateUpdated": "?string",
            "Version": "?string",
            "CreationTool": "?string",
            "DateCreated": "?string",
        }
        return yoda_schema

    def timeseriesresult(self):
        tsr_schema = {
            "ResultObj": self.result(),
            "XLocation": V.Nullable(V.AdaptTo(float)),
            "XLocationUnitsObj": V.Nullable(self.unit()),
            "YLocation": V.Nullable(V.AdaptTo(float)),
            "YLocationUnitsObj": V.Nullable(self.unit()),
            "ZLocation": V.Nullable(V.AdaptTo(float)),
            "ZLocationUnitsObj": V.Nullable(self.unit()),
            "SpatialReferenceObj": V.Nullable(self.spatialreference()),
            "IntendedTimeSpacing": V.Nullable(V.AdaptTo(float)),
            "IntendedTimeSpacingUnitsObj": V.Nullable(self.unit()),
            "AggregationStatisticCV": "string",
        }
        return tsr_schema

    def datasetcitation(self):
        dc_schema = {
            "DataSetObj": self.dataset(),
            "RelationshipTypeCV": "string",
            "CitationObj": self.citation(),
        }
        return dc_schema

    def personexternalidentifier(self):
        psi_schema = {
            "PersonObj": self.people(),
            "ExternalIdentifierSystemObj": self.externalidentifiersystem(),
            "PersonExternalIdentifier": "string",
            "PersonExternalIdentifierURI": "?string",
        }
        return psi_schema

    def timeseriesresultvalue(self):
        tsrv_schema = {
            "ColumnDefinitions": [
                {
                    "ColumnNumber": "integer",
                    "Label": "string",
                    "ODM2Field": "string",
                    "?QualityCodeCV": "string",
                    "?Result": self.timeseriesresult(),
                    "?CensorCodeCV": "string",
                    "?TimeAggregationInterval": V.AdaptTo(float),
                    "?TimeAggregationIntervalUnitsObj": self.unit(),
                }
            ], 
#            "Data": [[V.HeterogeneousSequence( "datacolumn1", "datacolumn2", "datacolumn3", "datacolumn3", "datacolumn3" )]],
#            "Data": [[( "datacolumn1", "datacolumn2", "datacolumn3", "datacolumn3", "datacolumn3" )]],
            "Data": [( "datacolumn1", "datacolumn2", "datacolumn3" )],
#            "Data": [[[ "string" ]]],
        }
        return tsrv_schema

    def authorlist(self):
        al_schema = {
            "CitationObj": self.citation(),
            "PersonObj": self.people(),
            "AuthorOrder": "integer",
        }
        return al_schema

    def spatialoffset(self):
        so_schema = {
            "SpatialOffsetTypeCV": "string",
            "Offset1Value": V.AdaptTo(float),
            "Offset1UnitObj": self.unit(),
            "Offset2Value": V.Nullable(V.AdaptTo(float)),
            "Offset2UnitObj": V.Nullable(self.unit()),
            "Offset3Value": V.Nullable(V.AdaptTo(float)),
            "Offset3UnitObj": V.Nullable(self.unit()),
        }
        return so_schema

    def relatedfeature(self):
        rf_schema = {
            "SamplingFeatureObj": self.samplingfeature(),
            "RelationshipTypeCV": "string",
            "RelatedFeatureObj": self.samplingfeature(),
            "SpatialOffsetObj": V.Nullable(self.spatialoffset()),
        }
        return rf_schema

    def actionby(self):
        ab_schema = {
            "ActionObj": self.action(),
            "AffiliationObj": self.affiliation(),
            "IsActionLead": "tobool",
            "RoleDescription": "?string",
        }
        return ab_schema

    def unit(self):
        unit_schema = {
            "UnitsTypeCV": "string",
            "UnitsAbbreviation": "string",
            "UnitsName": "string",
            "UnitsLink": "?string"
        }
        return unit_schema

    def taxonimicclassifier(self):
        tc_schema = {
            "TaxonomicClassifierTypeCV": "string",
            "TaxonomicClassifierName": "string",
            "TaxonomicClassifierCommonName": "?string",
            "TaxonomicClassifierDescription": "?string"
        }
        return tc_schema

    def relatedaction(self):
        ra_schema = {
            "RelationshipTypeCV": "string",
            "ActionObj": self.action(),
            "RelatedActionObj": self.action(),
        }
        return ra_schema

    def timeseries_schema(self):
        ts_schema = {
            "?YODA": [ self.yoda() ],
            # ODM2 core
            "Results": [ self.result() ],
            "Actions": [ self.action() ],
            "Methods": [ self.method() ],
            "SamplingFeatures": [ self.samplingfeature() ],
            "DataSets": [ self.dataset() ],
            "DataSetsResults": [ self.datasetresult() ],
            "ActionBy": [ self.actionby() ],
            "Affiliations": [ self.affiliation() ], 
            "FeatureActions": [ self.featureaction() ],
            "Organizations": [ self.organization() ],
            "People": [ self.people() ],
            "Variables": [ self.variable() ],
            "ProcessingLevels": [ self.processinglevel() ],
            "?Units": [self.unit()],
            "?TaxonomicClassifiers": [self.taxonimicclassifier()],
            "?RelatedActions": [self.relatedaction()],

            # ODM2 ExternalIdentifers
            "?ExternalIdentifierSystems": [ self.externalidentifiersystem() ],
            "?PersonExternalIdentifiers": [ self.personexternalidentifier()],
            "?SamplingFeatureExternalIdentifiers": [ self.sfexternalidentifier() ],

            # ODM2 Provenance
            "?AuthorLists": [ self.authorlist() ],
            "?Citations": [ self.citation() ],
            "?DataSetCitations": [ self.datasetcitation() ],

            # ODM2 SamplingFeatures
            "Sites": [ self.site() ],
            "?RelatedFeatures": [ self.relatedfeature() ],
            "?SpatialOffsets": [ self.spatialoffset() ],
            "?SpatialReferences": [ self.spatialreference() ],
            "?Specimens": [ self.specimen() ],

            # ODM2 Results
            "?TimeSeriesResults": [ self.timeseriesresult() ],
            # "?TimeSeriesResultValues": self.timeseriesresultvalue(),
        }
        return ts_schema

    def single_object_validate(self, schema, data, column=True):
        with V.parsing(required_properties=True,additional_properties=V.Object.REMOVE):
            validator = V.parse(schema)
        table_name = schema.keys()[0]
        col_name = ''
        if column:
            value = schema[table_name]
            for x in value:
                if isinstance(x, dict):
                    for key in x.keys():
                        col_name = '.%s' % key

        if table_name.startswith('?',0,1):
            table_name = table_name[1:]
        try:
            #print validator.is_valid(yaml_data)
            validator.validate(data)
            return '%s%s' % (table_name,col_name), True
        except (KeyError, ValueError, TypeError, ValidationError) as detail:
            return '%s%s: %s' % (table_name,col_name,detail), False

    def timeseries_detail_validate(self,data):
        flag = True
        ts_schema = self.timeseries_schema()
        for key in ts_schema.keys():
            schema = ts_schema[key][0]
            if key.startswith('?',0,1):
                table_name = key[1:]
                try:
                    table_data = data.pop(table_name)
                    table_data = {table_name:table_data}
                except KeyError:
                    #self.logger.info("there is no data for the table, '{0}'.".format(table_name))
                    continue
            else:
                table_data = data.pop(key)
                table_data = {key:table_data}
            for col_key in schema.keys():
                x,y = self.single_object_validate({key: [ {col_key: schema[col_key]} ]},table_data)
                if not y:
                    self.logger.error("%s" % x)
                    flag = False
        return flag

    def timeseries_object_validate(self,data):
        flag = True
        ts_schema = self.timeseries_schema()
        for key in ts_schema.keys():
            if key.startswith('?',0,1):
                table_name = key[1:]
                try:
                    table_data = data.pop(table_name)
                    table_data = {table_name:table_data}
                except KeyError:
                    #self.logger.info("there is no data for the table, '{0}'.".format(table_name))
                    continue
            else:
                table_data = data.pop(key)
                table_data = {key:table_data}
            x,y = self.single_object_validate({key: ts_schema[key]},table_data,False)
            if not y:
                self.logger.error("%s" % x)
                flag = False
        return flag