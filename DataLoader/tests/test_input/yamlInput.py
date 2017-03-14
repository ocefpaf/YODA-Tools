from DataLoader.Model.Inputs.yamlInput import yamlInput


class TestYaml:
    def setup(self):

        self.yi = yamlInput()

    def test_parse_ts(self):
        self.file_path = "../test_files/test_ts.yaml"
        self.yi.parse(self.file_path)
        session = self.yi.sendODM2Session
        print session
        assert session != None
        # assert  != None

    def test_parse_specimen(self):
        self.file_path = "../test_files/test_specimen_ts.yaml"
        self.yi.parse(self.file_path)
        session = self.yi.sendODM2Session
        print session
        assert session != None




