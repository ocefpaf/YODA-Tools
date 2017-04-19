
from odm2api.ODM2.models import Base

class iOutputs():

    def parseObjects(self, session):
        data = {}
        for t in self.get_table_names():
            tmplist = []
            try:
                for o in session.query(t).all():
                    tmplist.append(o)
            except Exception as e:
                print e
            data[t.__class__.__name__] = tmplist
        return data

    def get_table_names(self):
        tables = []
        import inspect
        import sys
        # get a list of all of the classes in the module
        clsmembers = inspect.getmembers(sys.modules["odm2api.ODM2.models"],
                                        lambda member: inspect.isclass(member) and member.__module__ == "odm2api.ODM2.models")

        for name, Tbl in clsmembers:
            import sqlalchemy.ext.declarative.api as api
            if isinstance(Tbl, api.DeclarativeMeta):
                # check to see if the schema is already set correctly
                tables.append(Tbl)
        return tables

    def save(self, session, file_path):
        raise NotImplementedError()

    def accept(self):
        raise NotImplementedError()
