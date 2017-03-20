from DataLoader.model.Outputs.yamlOutput import yamlOutput
from DataLoader.tests.test_util import build_ts_session, build_ts_sepecimen_db

import os
curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class TestYaml:
    def setup(self):
        self.yo = yamlOutput()

    def test_create_ts(self):
        session = build_ts_session()
        file_path = r"D:\DEV\test_ts.yaml"
        self.yo.save(session, file_path)

    def test_create_specimen(self):
        session = build_ts_sepecimen_db()
        file_path = r"D:\DEV\test_ts_specimen.yaml"
        self.yo.save(session, file_path)
