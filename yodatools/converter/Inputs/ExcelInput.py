import os
import openpyxl
from odm2api.ODM2.models import *
from yodatools.converter.Abstract import iInputs
import pandas


class ExcelInput(iInputs):
    def __init__(self, input_file, output_file=None):
        super(ExcelInput, self).__init__()

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

    def parse(self, file_path=None, db_conn = None):
        if not self.verify(file_path):
            print "Something is wrong with the file but what?"
            return

        self.tables = self.get_table_name_ranges()
        methods = self.parse_methods()
        variables = self.parse_variables()
        units = self.parse_units()
        processing_levels = self.parse_processing_level()
        sampling_feature = self.parse_sampling_feature()
        affiliations = self.parse_affiliations()

        self._session.add_all(methods)
        self._session.add_all(variables)
        self._session.add_all(units)
        self._session.add_all(processing_levels)
        self._session.add_all(sampling_feature)
        self._session.add_all(affiliations)

    def parse_sites(self):
        return self.parse_sampling_feature()

    def parse_units(self):
        CONST_UNITS = 'Units'

        sheet, tables = self.get_sheet_and_table(CONST_UNITS)

        if not len(tables):
            return []

        units = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                unit = Units()
                unit.UnitsTypeCV = row[0].value
                unit.UnitsAbbreviation = row[1].value
                unit.UnitsName = row[2].value
                unit.UnitsLink = row[3].value
                units.append(unit)

        return units

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

        def parse_organizations(table):
            organizations = {}
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            for row in cells:
                org = Organizations()
                org.OrganizationTypeCV = row[0].value
                org.OrganizationCode = row[1].value
                org.OrganizationName = row[2].value
                org.OrganizationDescription = row[3].value
                org.OrganizationLink = row[4].value

                organizations[org.OrganizationName] = org

            return organizations

        def parse_authors(table):
            authors = []
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
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
                orgs = parse_organizations(table)

        for aff in affiliations:
            if aff.OrganizationObj.OrganizationName in orgs:
                aff.OrganizationObj = orgs[aff.OrganizationObj.OrganizationName]

        return affiliations

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

        return processing_levels

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
                sf.SamplingFeatureUUID = row[0]
                sf.SamplingFeatureCode = row[1]
                sf.SamplingFeatureName = row[2]
                sf.SamplingFeatureDescription = row[3]
                sf.FeatureGeometryWKT = row[4]
                sf.Elevation_m = row[5]
                sf.SamplingFeatureTypeCV = row[6]
                sampling_features.append(sf)

        return sampling_features

    def parse_specimens(self):
        SPECIMENS = 'Specimens'
        sheet, tables = self.get_sheet_and_table(SPECIMENS)

        if not len(tables):
            return []

        specimens = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                sp = Specimens()
                sp.SamplingFeatureUUID = row[0].value
                sp.SamplingFeatureCode = row[1].value
                sp.SamplingFeatureName = row[2].value
                sp.SamplingFeatureDescription = row[3].value
                sp.SamplingFeatureTypeCV = row[4].value
                sp.SpecimenMediumCV = row[5].value
                sp.IsFieldSpecimen = row[6].value
                specimens.append(sp)

        return specimens

    def parse_methods(self):
        CONST_METHODS = "Methods"
        sheet, tables = self.get_sheet_and_table(CONST_METHODS)

        if not len(tables):
            return []

        methods = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]

            for row in cells:
                method = Methods()
                method.MethodTypeCV = row[0].value
                method.MethodCode = row[1].value
                method.MethodName = row[2].value
                method.MethodDescription = row[3].value
                method.MethodLink = row[4].value

                org = Organizations()
                org.OrganizationName = row[5].value
                method.OrganizationObj = org

                methods.append(method)

        return methods

    def parse_variables(self):

        CONST_VARIABLES = "Variables"

        if CONST_VARIABLES not in self.tables:
            return []

        sheet = self.workbook.get_sheet_by_name(CONST_VARIABLES)
        tables = self.tables[CONST_VARIABLES]

        variables = []
        for table in tables:
            cells = sheet[table.attr_text.split('!')[1].replace('$', '')]
            for row in cells:
                var = Variables()
                var.VariableTypeCV = row[0].value
                var.VariableCode = row[1].value
                var.VariableNameCV = row[2].value
                var.VariableDefinition = row[3].value
                var.SpeciationCV = row[4].value
                var.NoDataValue = row[5].value
                variables.append(var)

        return variables

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
