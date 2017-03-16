from DataLoader.model.Inputs.yamlInput import yamlInput

import os

curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class TestYaml:

    def setup(self):
        self.yi = yamlInput()

    def test_parse_ts(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_ts.yaml')
        self.yi.parse(file_path)

        session = self.yi.sendODM2Session()
        print session
        assert session != None
        assert len(session.dirty)>0;



    def test_parse_specimen(self):
        file_path = os.path.join(curr_folder, 'test_files', 'test_specimen_ts.yaml')

        self.yi.parse(file_path)
        session = self.yi.sendODM2Session()

        assert session != None
        assert len(session.dirty) > 0;




