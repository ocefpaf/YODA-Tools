
from odm2api.ODM2.models import Base
from odm2api.ODMconnection import dbconnection


def build_db(engine):

    # create connection to temp sqlite db
    session_factory = dbconnection.createConnection('sqlite', 'D:/DEV/ODM2.sqlite', 2.0)
    _engine = session_factory.engine
    Base.metadata.create_all(_engine)


def build_session(session_factory):
    # get
    # persons = _session.query(People).limit(50).all()
    # datasets = _session.query(DataSets).limit(50).all()
    # citations = _session.query(Citations).limit(50).all()
    # authorlists = _session.query(AuthorLists).limit(50).all()
    # spatial_references = _session.query(SpatialReferences).limit(50).all()
    #
    # sampling_features = _session.query(SamplingFeatures).limit(50).all()
    #
    # sites = _session.query(Sites).limit(50).all()
    #
    # methods = _session.query(Methods).limit(50).all()
    # variables = _session.query(Variables).limit(50).all()
    # units = _session.query(Units).limit(50).all()
    # processing_levels = _session.query(ProcessingLevels).limit(50).all()
    # actions = _session.query(Actions).limit(50).all()
    # results = _session.query(Results).limit(50).all()
    # # noinspection PyUnboundLocalVariable
    # time_series_results = _session.query(TimeSeriesResults).limit(50).all()
    # time_series_result_values = _session.query(TimeSeriesResultValues).limit(50).all()

    pass


