from DataLoader.model.Inputs.yamlInput import yamlInput
from DataLoader.tests.test_util import build_session

import os

curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class TestYaml:

    def setup(self):
        self.yi = yamlInput()

    def test_parse_ts(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_ts.yaml')
        self.yi.parse(file_path)

        session = self.yi.sendODM2Session()

        assert session != None
        from odm2api.ODM2.models import People
        assert len(session.query(People).all()) > 0

    def test_parse_specimen(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_specimen_ts.yaml')

        self.yi.parse(file_path)
        session = self.yi.sendODM2Session()

        assert session != None
        from odm2api.ODM2.models import People
        assert len(session.query(People).all()) > 0




