from DataLoader.model.Outputs import yamlOutput
from DataLoader.tests.test_util import build_session

import os

curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class TestYaml:
    def setup(self):
        self.session = build_session()


    def test_parse_ts(self):
        pass