
# Supporting Python3
try:
    import urllib.request as request
except ImportError:
    import urllib as request
import xml.etree.ElementTree as ET
import odm2api.ODM2.models as odm2model

url = "http://vocabulary.odm2.org/api/v1/%s/?format=skos"

vocab= {"ActionTypeCV": "actiontype",
        "QualityCodeCV": "qualitycode",
        "SamplingFeatureGeotypeCV": "samplingfeaturegeotype",
        "ElevationDatumCV": "elevationdatum",
        "ResultTypeCV": "resulttype",
        #("sampledmedium", CVSampledMedium),
        "SpeciationCV": "speciation",
        "AggregationStatisticCV": "aggregationstatistic",
        "MethodTypeCV": "methodtype",
        "TaxonomicClassifierTypeCV": "taxonomicclassifiertype",
        "SiteTypeCV": "sitetype",
        "CensorCodeCV": "censorcode",
        "DirectiveTypeCV": "directivetype",
        "DataSetTypeCV": "datasettype",
        "DataQualityTypeCV": "dataqualitytype",
        "OrganizationTypeCV": "organizationtype",
        "StatusCV": "status",
        "AnnotationTypeCV": "annotationtype",
        "SamplingFeatureTypeCV": "samplingfeaturetype",
        "EquipmentTypeCV": "equipmenttype",
        #("specimenmedium", CVSpecimenMedium),
        "SpatialOffsetTypeCV": "spatialoffsettype",
        #("referencematerialmedium", CVReferenceMaterialMedium),
        "SpecimenTypeCV": "specimentype",
        "VariableTypeCV": "variabletype",
        "VariableNameCV": "variablename",
        "PropertyDataTypeCV": "propertydatatype",
        "RelationshipTypeCV": "relationshiptype",
        "UnitsTypeCV": "unitstype",
        "SampledMediumCV": "medium"
        }

#XML encodings
dc = "{http://purl.org/dc/elements/1.1/}%s"
rdf = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}%s"
skos = "{http://www.w3.org/2004/02/skos/core#}%s"
odm2 = "{http://vocabulary.odm2.org/ODM2/ODM2Terms/}%s"

class CVvalidator(object):

    def __init__(self,logger):
        self.logger = logger

    def cv_names(self,attr):
        names = []
        key = vocab[attr]
        data = request.urlopen(url % key).read()
        root = ET.fromstring(data)
        for voc in root.findall(rdf %"Description"):
            #Term = voc.attrib[rdf%"about"].split('/')[-1]
            #print "Term: %s" % Term
            if voc.find(skos%"prefLabel") is not None:
                Name = voc.find(skos%"prefLabel").text
                names.append(Name.lower())
        return names

    def get_cv_attrs(self,cls_name):
        obj = getattr(odm2model,cls_name)
        return [i for i in obj.__dict__.keys() if i[:1] != '_' and i.endswith("CV")]

    def validate(self,data):
        flag = True
        timeSeries = None
        if "TimeSeriesResultValues" in data:
            timeSeries = data.pop('TimeSeriesResultValues')
            timeSeries = timeSeries.pop('ColumnDefinitions')

        for key in data.keys():
            cv_attrs = self.get_cv_attrs(key)
            if cv_attrs is not None and len(cv_attrs) > 0:
                for cv_attr in cv_attrs:
                    cv_names = self.cv_names(cv_attr)
                    for attr in data[key]:
                        try:
                            value = attr[cv_attr]
                            if value and (not value.lower() in cv_names):
                                flag = False
                                self.logger.error("'%s.%s': '%s' is not in vocaburary list." % (key,cv_attr,value))
                        except KeyError:
                            self.logger.info("'%s.%s' is not existed." % (cv_attr,key))

        cv_attrs = self.get_cv_attrs("TimeSeriesResultValues")
        if cv_attrs is not None and len(cv_attrs) > 0:
            for cv_attr in cv_attrs:
                cv_names = self.cv_names(cv_attr)
                for attr in timeSeries:
                    try:
                        if attr['ODM2Field'] == 'DataValue':
                            value = attr[cv_attr]
                            if value and (not value.lower() in cv_names):
                                flag = False
                                self.logger.error("'TimeSeriesResultValues.%s': '%s' is not in vocaburary list." % (cv_attr,value))
                    except KeyError:
                        flag = False
                        self.logger.info("'TimeSeriesResultValues.%s' is not existed." % cv_attr)
        return flag
