
from DataLoader.model.Abstract import iOutputs
from yodaloader.YAML.yamlFunctions import YamlFunctions


class yamlOutput(iOutputs):

    def save(self, session):
        tables = self.parseObjects()
        print tables

    def accept(self):
        raise NotImplementedError()

