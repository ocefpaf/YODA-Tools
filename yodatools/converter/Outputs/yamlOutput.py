import yaml

from yodatools.converter.Abstract import iOutputs


class yamlOutput(iOutputs):

    def save(self, session, file_path):
        tables = self.parseObjects()
        data = []
        for t in tables:
            try:
                for o in session.query(t).all():
                    data.append(o)
            except Exception as e:
                print e
        with open(file_path, "w+") as f:
            f.write("test")
            yaml.dump_all(data, f)

    def accept(self):
        raise NotImplementedError()

