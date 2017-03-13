from DataLoader.Model.Inputs.yamlInput import yamlInput


class TestYaml:
    def setup(self):
        self.file_path = r"D:\DEV\YODA-Tools\yodaLoader\test.yaml"
        self.yi = yamlInput()

    def test_parse_yaml(self):
        self.yi.parse_file(self.file_path)
        session = self.yi.sendODM2Session
        print session
        assert session != None
        # assert  != None
