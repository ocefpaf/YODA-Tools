from DataLoader.Model.Inputs.yamlInput import yamlInput

import os

curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class TestYaml:

    def setup(self):
        self.yi = yamlInput()

    def test_parse_ts(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_ts.yaml')
        print file_path
        # self.file_path = "../test_files/test_ts.yaml"
        self.yi.parse(file_path)
        session = self.yi.sendODM2Session
        print session
        assert session != None
        # assert  != None

    def test_parse_specimen(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_specimen_ts.yaml')

        # self.file_path = "../test_files/test_specimen_ts.yaml"
        self.yi.parse(file_path)
        session = self.yi.sendODM2Session
        print session
        assert session != None




