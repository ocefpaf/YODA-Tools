import os

from tests.test_util import build_ts_session, build_ts_specimen_session
from yodatools.converter.Outputs.dbOutput import dbOutput
from odm2api import ODMconnection


curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# curr_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# file_path = os.path.join(curr_folder, 'test_files', 'YODA_TimeSeriesSpecimen_RB_2014-15_pub.xlsx')
class TestDb:
    def setup(self):

        self.connection_string = 'mysql+pymysql://Bob:odm@localhost/bobrules'
        self.do = dbOutput(self.connection_string)



    def test_create_specimen(self):
        session = build_ts_specimen_session()
        self.do.save(session, self.connection_string)


    def test_create_ts(self):
        session = build_ts_session()
        # self.dhttp://www.pcgamer.com/meet-the-man-who-loved-stardew-valley-so-much-he-bought-a-farm/o.save(session, self.connection_string)