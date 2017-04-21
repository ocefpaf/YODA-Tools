import os
import openpyxl
from odm2api.ODM2.models import *
from yodatools.converter.Abstract import iInputs
import pandas


class ExcelInput(iInputs):
    def __init__(self, input_file, output_file=None):
        super(ExcelInput, self).__init__()
        self.create_memory_db()
        self.input_file = input_file

        if output_file is None:
            output_file = "export.csv"

        self.output_file = output_file
        self.workbook = None
        self.sheets = []
        self.name_ranges = None
        self.tables = {}

    def get_table_name_ranges(self):
        """
        Returns a list of the name range that have a table.
        The name range should contain the cells locations of the data.
        :rtype: list
        """
        CONST_NAME = "_Table"
        table_name_range = {}
        for name_range in self.name_ranges:
            if CONST_NAME in name_range.name:
                sheet = name_range.attr_text.split('!')[0]
                sheet = sheet.replace('\'', '')

                if sheet in table_name_range:
                    table_name_range[sheet].append(name_range)
                else:
                    table_name_range[sheet] = [name_range]

        return table_name_range

    def parse(self, file_path=None):
        if not self.verify(file_path):
            print "Something is wrong with the file but what?"
            return

        self.tables = self.get_table_name_ranges()

        self.parse_affiliations()
        self.parse_methods()
        self.parse_variables()
        self.parse_units()
        self.parse_processing_level()
        self.parse_sampling_feature()
        self.parse_specimens()
        self.parse_analysis_results()

    def parse_analysis_results(self):
        SHEET_NAME = "Analysis_Results"
        sheet, tables = self.get_sheet_and_table(SHEET_NAME)

        if not len(tables):
            return

        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            for row in cells:
                result = Results()
                action = Actions()
                feat_act = FeatureActions()
                act_by = ActionBy()
                measure_result = MeasurementResults()
                measure_result_value = MeasurementResultValues()

                # First the results
                variable = self._session.query(Variables).filter_by(VariableCode=row[2].value).first()
                units = self._session.query(Units).filter_by(UnitsName=row[4].value).first()
                proc_level = self._session.query(ProcessingLevels).filter_by(ProcessingLevelCode=row[11].value).first()

                result.ResultUUID = row[0].value
                result.VariableObj = variable
                result.VariableID = variable.VariableID
                result.UnitsID = units.UnitsID
                result.ProcessingLevelObj = proc_level
                result.ProcessingLevelID = proc_level.ProcessingLevelID
                result.SampledMediumCV = row[12].value

                # Feature Actions
                feat_act.SamplingFeatureID = row[1].value

                # Measurements Result Value
                measure_result_value.DataValue = row[3].value
                measure_result_value.ValueDateTime = row[5].value
                measure_result_value.ValueDateTimeUTCOffset = row[6].value

                # Measurement Result (Different from Measurement Result Value)
                units = self._session.query(Units).filter_by(UnitsName=row[14].value).first()

                measure_result.CensorCodeCV = row[9].value
                measure_result.QualityCodeCV = row[10].value
                measure_result.TimeAggregationInterval = row[13].value
                measure_result.TimeAggregationIntervalUnitsObj = units
                measure_result.TimeAggregationIntervalUnitsID = units.UnitsID
                measure_result.AggregationStatisticCV = row[15].value

                # Action
                method = self._session.query(Methods).filter_by(MethodCode=row[7].value).first()
                action.MethodObj = method
                action.MethodID = method.MethodID

                # Action By
                first_name, last_name = row[8].value.split(' ')
                person = self._session.query(People).filter_by(PersonLastName=last_name).first()
                affiliations = self._session.query(Affiliations).filter_by(PersonID=person.PersonID).first()
                act_by.AffiliationObj = affiliations
                act_by.AffiliationID = affiliations.AffiliationID

                # Link together
                result.FeatureActionID = feat_act.FeatureActionID
                result.FeatureActionObj = feat_act

                pass

        pass

    def parse_sites(self):
        return self.parse_sampling_feature()

    def parse_units(self):
        CONST_UNITS = 'Units'

        sheet, tables = self.get_sheet_and_table(CONST_UNITS)

        if not len(tables):
            return

        units = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                unit = Units()
                unit.UnitsTypeCV = row[0].value
                unit.UnitsAbbreviation = row[1].value
                unit.UnitsName = row[2].value
                unit.UnitsLink = row[3].value

                if unit.UnitsTypeCV is not None:
                    units.append(unit)

        self._session.add_all(units)
        self._session.flush()

    def read_data_values(self):
        dataframes = pandas.read_excel(io=self.input_file, sheetname='Data Values')
        # dataframes.transpose()
        dataframes = dataframes.set_index(['LocalDateTime'])
        unstacked_dataframes = dataframes.unstack()
        avg = unstacked_dataframes['AirTemp_Avg']
        # avg.values
        print dataframes

    def parse_affiliations(self):  # rename to Affiliations
        SHEET_NAME = 'People and Organizations'
        sheet, tables = self.get_sheet_and_table(SHEET_NAME)

        if not len(tables):
            return []

        def parse_organizations(org_table, session):
            organizations = {}

            cells = sheet[org_table.attr_text.split('!')[1].replace('$', '')]
            for row in cells:
                org = Organizations()
                org.OrganizationTypeCV = row[0].value
                org.OrganizationCode = row[1].value
                org.OrganizationName = row[2].value
                org.OrganizationDescription = row[3].value
                org.OrganizationLink = row[4].value
                session.add(org)
                organizations[org.OrganizationName] = org

            return organizations

        def parse_authors(author_table):
            authors = []
            cells = sheet[author_table.attr_text.split('!')[1].replace('$', '')]
            for row in cells:
                ppl = People()
                org = Organizations()
                aff = Affiliations()

                ppl.PersonFirstName = row[0].value
                ppl.PersonMiddleName = row[1].value
                ppl.PersonLastName = row[2].value

                org.OrganizationName = row[3].value
                aff.AffiliationStartDate = row[5].value
                aff.AffiliationEndDate = row[6].value
                aff.PrimaryPhone = row[7].value
                aff.PrimaryEmail = row[8].value
                aff.PrimaryAddress = row[9].value
                aff.PersonLink = row[10].value

                aff.OrganizationObj = org
                aff.PersonObj = ppl

                authors.append(aff)
            return authors

        # Combine table and authors

        orgs = {}
        affiliations = []
        for table in tables:
            if 'Authors_Table' == table.name:
                affiliations = parse_authors(table)
            else:
                orgs = parse_organizations(table, self._session)

        self._session.flush()

        for aff in affiliations:
            if aff.OrganizationObj.OrganizationName in orgs:
                aff.OrganizationObj = orgs[aff.OrganizationObj.OrganizationName]

        self._session.add_all(affiliations)
        self._session.flush()

    def get_sheet_and_table(self, sheet_name):
        if sheet_name not in self.tables:
            return [], []
        sheet = self.workbook.get_sheet_by_name(sheet_name)
        tables = self.tables[sheet_name]

        return sheet, tables

    def parse_processing_level(self):
        CONST_PROC_LEVEL = 'Processing Levels'
        sheet, tables = self.get_sheet_and_table(CONST_PROC_LEVEL)

        if not len(tables):
            return []

        processing_levels = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                proc_lvl = ProcessingLevels()
                proc_lvl.ProcessingLevelCode = row[0].value
                proc_lvl.Definition = row[1].value
                proc_lvl.Explanation = row[2].value
                processing_levels.append(proc_lvl)

        # return processing_levels
        self._session.add_all(processing_levels)
        self._session.flush()

    def parse_sampling_feature(self):
        SAMP_FEAT = 'Sampling Features'

        if SAMP_FEAT not in self.tables:
            if 'Sites' in self.tables:
                SAMP_FEAT = 'Sites'
            else:
                return []

        sheet = self.workbook.get_sheet_by_name(SAMP_FEAT)
        tables = self.tables[SAMP_FEAT]

        sampling_features = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                sf = SamplingFeatures()
                sf.SamplingFeatureUUID = row[0].value
                sf.SamplingFeatureCode = row[1].value
                sf.SamplingFeatureName = row[2].value
                sf.SamplingFeatureDescription = row[3].value
                sf.FeatureGeometryWKT = row[4].value
                sf.Elevation_m = row[5].value
                sf.SamplingFeatureTypeCV = row[6].value
                sampling_features.append(sf)

        self._session.add_all(sampling_features)
        self._session.flush(sampling_features)

    def parse_specimens(self):
        SPECIMENS = 'Specimens'
        sheet, tables = self.get_sheet_and_table(SPECIMENS)

        if not len(tables):
            return []

        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                sp = Specimens()
                a = Actions()
                rf = RelatedFeatures()

                # First the Specimen/Sampling Feature
                sp.SamplingFeatureUUID = row[0].value
                sp.SamplingFeatureCode = row[1].value
                sp.SamplingFeatureName = row[2].value
                sp.SamplingFeatureDescription = row[3].value
                sp.SamplingFeatureTypeCV = row[4].value
                sp.SpecimenMediumCV = row[5].value
                sp.IsFieldSpecimen = row[6].value
                sp.ElevationDatumCV = 'unknown'
                sp.SpecimenTypeCV = 'grab'
                sp.SpecimenMediumCV = 'liquidAqueous'

                # Next is Related Features
                rf.RelationshipTypeCV = 'wasCollectedAt'
                # rf.RelatedFeatureID is the CollectionSite.
                # Query the site id using the collection site (which is the site code aka Sampling Feature Code)
                # Link things together
                sampling_feature = self._session.query(SamplingFeatures).filter_by(SamplingFeatureCode=row[7].value).first()
                rf.SamplingFeatureID = sampling_feature.SamplingFeatureID
                rf.RelatedFeatureID = row[7].value
                # rf.RelatedFeatureID = needs to be set...

                # Last is the Action/SampleCollectionAction
                a.ActionTypeCV = 'specimenCollection'
                a.BeginDateTime = row[8].value
                a.BeginDateTimeUTCOffset = row[9].value
                method = self._session.query(Methods).filter_by(MethodCode=row[10].value).first()
                a.MethodID = method.MethodID

                self._session.add(sp)
                self._session.add(a)
                self._session.add(rf)

        self._session.flush()  # Need to set the RelatedFeature.RelatedFeatureID before flush will work

    def parse_methods(self):
        CONST_METHODS = "Methods"
        sheet, tables = self.get_sheet_and_table(CONST_METHODS)

        if not len(tables):
            return []

        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                method = Methods()
                method.MethodTypeCV = row[0].value
                method.MethodCode = row[1].value
                method.MethodName = row[2].value
                method.MethodDescription = row[3].value
                method.MethodLink = row[4].value

                # If organization does not exist then it returns None
                org = self._session.query(Organizations).filter_by(OrganizationName=row[5].value).first()
                method.OrganizationObj = org

                if method.MethodCode:  # Cannot store empty/None objects
                    self._session.add(method)

        self._session.flush()

    def parse_variables(self):

        CONST_VARIABLES = "Variables"

        if CONST_VARIABLES not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_VARIABLES)
        tables = self.tables[CONST_VARIABLES]

        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            for row in cells:
                var = Variables()
                var.VariableTypeCV = row[0].value
                var.VariableCode = row[1].value
                var.VariableNameCV = row[2].value
                var.VariableDefinition = row[3].value
                var.SpeciationCV = row[4].value

                if row[5].value is not None:
                    var.NoDataValue = None if row[5].value == 'NULL' else row[5].value

                if var.NoDataValue is not None:  # NoDataValue cannot be None
                    self._session.add(var)

        self._session.flush()

    def verify(self, file_path=None):

        if file_path is not None:
            self.input_file = file_path

        if not os.path.isfile(self.input_file):
            print "File does not exist"
            return False

        self.workbook = openpyxl.load_workbook(self.input_file, read_only=True)
        self.name_ranges = self.workbook.get_named_ranges()
        self.sheets = self.workbook.get_sheet_names()

        return True

    def sendODM2Session(self):
        return self._session
