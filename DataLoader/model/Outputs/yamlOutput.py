
from DataLoader.model.Abstract import iOutputs
from yodaloader.YAML.yamlFunctions import YamlFunctions


class yamlOutput(iOutputs):

    def save(self, session):
        tables = self.parseObjects()


    def accept(self):
        raise NotImplementedError()