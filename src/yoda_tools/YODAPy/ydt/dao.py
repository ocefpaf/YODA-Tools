
class BaseXldao(object):

    def get_yoda_header(self):
        """
        Returns yoda header in the data source.
        """
        raise NotImplementedError("get_yoda_header Method not implemented by this service.")

    def get_all_people(self):
        """
        Returns people in the data source.
        """
        raise NotImplementedError("get_people Method not implemented by this service.")

    def get_all_organizations(self):
        """
        Returns organizations in the data source.
        """
        raise NotImplementedError("get_organizations Method not implemented by this service.")

    def get_all_affiliations(self):
        """
        Returns people in the data source.
        """
        raise NotImplementedError("get_people Method not implemented by this service.")

    def get_dataset(self):
        """
        Returns dataset in the data source.
        """
        raise NotImplementedError("get_dataset Method not implemented by this service.")

    def get_citation(self):
        """
        Returns external citation in the data source.
        """
        raise NotImplementedError("get_citation Method not implemented by this service.")

    def get_datasetcitation(self):
        """
        Returns external citation in the data source.
        """
        raise NotImplementedError("get_citation Method not implemented by this service.")

    def get_all_authorlists(self):
        """
        Returns authors in the data source.
        """
        raise NotImplementedError("get_all_authors Method not implemented by this service.")

    def get_all_samplingfeatures(self):
        """
        Returns sampling features in the data source.
        """
        raise NotImplementedError("get_all_samplingfeatures Method not implemented by this service.")

    def get_all_child_samplingfeatures(self):
        """
        Returns child sampling features in the data source.
        """
        raise NotImplementedError("get_all_child_samplingfeatures Method not implemented by this service.")

    def get_all_sites(self):
        """
        Returns sites in the data source.
        """
        raise NotImplementedError("get_all_sites Method not implemented by this service.")

    def get_all_specimens(self):
        """
        Returns specimens in the data source.
        """
        raise NotImplementedError("get_all_specimens Method not implemented by this service.")

    def get_all_spatialoffsets(self):
        """
        Returns spatial offsets in the data source.
        """
        raise NotImplementedError("get_all_spatialoffsets Method not implemented by this service.")

    def get_all_relatedfeatures(self):
        """
        Returns related features in the data source.
        """
        raise NotImplementedError("get_all_relatedfeatures Method not implemented by this service.")

    def get_all_actions(self):
        """
        Returns actions in the data source.
        """
        raise NotImplementedError("get_all_actions Method not implemented by this service.")

    def get_all_actionbys(self):
        """
        Returns action by in the data source.
        """
        raise NotImplementedError("get_all_actionbys Method not implemented by this service.")

    def get_all_featureactions(self):
        """
        Returns feature action in the data source.
        """
        raise NotImplementedError("get_all_featureactions Method not implemented by this service.")

    def get_all_results(self):
        """
        Returns results in the data source.
        """
        raise NotImplementedError("get_all_results Method not implemented by this service.")

    def get_all_measurementresults(self):
        """
        Returns measurement results in the data source.
        """
        raise NotImplementedError("get_all_measurementresults Method not implemented by this service.")

    def get_all_measurementresultvalues(self):
        """
        Returns measurement result values in the data source.
        """
        raise NotImplementedError("get_all_measurementresultvalues Method not implemented by this service.")

    def get_all_methods(self):
        """
        Returns methods in the data source.
        """
        raise NotImplementedError("get_all_methods Method not implemented by this service.")

    def get_all_variables(self):
        """
        Returns variables in the data source.
        """
        raise NotImplementedError("get_all_variables Method not implemented by this service.")

    def get_all_processinglevels(self):
        """
        Returns processing levels in the data source.
        """
        raise NotImplementedError("get_all_processinglevels Method not implemented by this service.")

    def get_all_datacolumns(self):
        """
        Returns data columns in the data source.
        """
        raise NotImplementedError("get_all_datacolumns Method not implemented by this service.")

    def get_all_datavalues(self):
        """
        Returns data values in the data source.
        """
        raise NotImplementedError("get_all_datavalues Method not implemented by this service.")

    def get_all_spatialreferences(self):
        """
        Returns Spatial References in the data source.
        """
        raise NotImplementedError("get_all_spatialreferences Method not implemented by this service.")

    def get_all_externalidentifiers(self):
        """
        Returns External Identifiers in the data source.
        """
        raise NotImplementedError("get_all_externalidentifiers Method not implemented by this service.")

    def get_all_personexternalidentifiers(self):
        """
        Returns Person External Identifiers in the data source.
        """
        raise NotImplementedError("get_all_personexternalidentifiers Method not implemented by this service.")
