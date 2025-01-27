from collections import OrderedDict
from datetime import date
from typing import Union, List, Any

from src.cmdb_exchange.builders.parsers import FlatDataParser, \
    CmdbDataFileParser, ContactFileParser


class BaseBuilder:
    """
    The base class specifies methods for creating a file and get information from it.
    """

    @property
    def file_name(self):
        """
        File name required parameter. If the file name contains a variable part, for example date,
        then replace this part with '*'. For example if the filename is 'Export_20201210',
        then specify 'Export_*'.
        """
        raise NotImplementedError

    @property
    def fields(self):
        """
        A dictionary that contains the name of the model field as a key and
        the corresponding header in the file as a value.
        """
        raise NotImplementedError

    def __init__(self):
        self._flatten = FlatDataParser()
        self._parser = None

    def get_data(self, data: list) -> list:
        return self._parser.export_data(data)

    def set_fields_name(self, data: dict) -> dict:
        """
        Takes a data dictionary from a file and replaces the headers with their
        corresponding keys from 'fields'

        :param data: dict. Dictionary with keys given from file
        :return: dict. Dictionary with keys corresponding the model fields
        """
        new_row = {}
        for k, v in self.fields.items():
            for row_k, row_v in data.items():
                if row_k == v:
                    new_row[k] = row_v
        return new_row

    def export_data(self, data: list) -> Union[list, List[dict]]:
        """
        Extracts the fields from the received object that needs to create the file.
        Flattens a dictionary with the nested structure to a dictionary with no hierarchy.

        :param data: list. List of dict with full information
        :return: list. List of dict with prepared to export data
        """
        nested_data = self.get_data(data)
        for row in nested_data:
            self._flatten.visit(row)
        return self._flatten.result

    def import_data(self, data: list) -> Any:
        """
        Replaces headers in the data read from the file with the corresponding keys
        and parses the necessary data using '_parser'
        :param data: list. List of data read from file
        :return: dict.
        """
        for i, row in enumerate(data):
            data[i] = self.set_fields_name(row)
        return self._parser.import_data(data)

    def generate_filename(self) -> str:
        """
        Replacing a '*' symbol from 'file_name' to current date in "YYYYMMDD" format.
        :return: str. Filename with current date
        """
        today = date.today()
        return self.file_name.replace('*', today.strftime('%Y%m%d'))


class EnvironmentUsersBuilder(BaseBuilder):

    file_name = 'AppSearchContactExport_*_Environment'

    fields = OrderedDict((
        ('ciid', 'CIID'),
        ('name', 'Application Name'),
        ('user_name', 'Contact  Name'),
        ('type', 'CI Contact Type'),
        ('phone', 'Contact Phone'),
        ('email', 'Email'),
        ('id', 'SC Contact ID'),
        ('status', 'Contact Status'),
        ('comments', 'Comments')
    ))

    def __init__(self):
        super().__init__()
        self._parser = ContactFileParser(keys=self.fields.keys())

    def get_data(self, data: list) -> list:
        result = []
        for row in data:
            data = self._parser.export_data(row.get('environments'))
            result.extend(data)
        return result


class MasterUsersBuilder(BaseBuilder):

    file_name = 'AppSearchContactExport_*_Master'

    fields = OrderedDict((
        ('master_ciid', 'CIID'),
        ('application', 'Application Name'),
        ('user_name', 'Contact  Name'),
        ('type', 'CI Contact Type'),
        ('phone', 'Contact Phone'),
        ('email', 'Email'),
        ('id', 'SC Contact ID'),
        ('status', 'Contact Status'),
        ('comments', 'Comments')
    ))

    def __init__(self):
        super().__init__()
        self._parser = ContactFileParser(keys=self.fields.keys())


class CmdbDataBuilder(BaseBuilder):

    file_name = 'cmdb-sample-download'

    fields = OrderedDict((
        ('ciid', 'CIID'),
        ('master_ciid', 'Master CI ID'),
        ('application', 'Application Name'),
        ('name', 'Deployment Name'),
        ('description', 'Deployment Description'),
        ('status', 'Status'),
        ('env_type', 'Env. Type'),
        ('app_deployment_type', 'Application Deployment Type'),
        ('location', 'Location'),
        ('org_level_1', 'Org Level 1'),
        ('org_level_2', 'Org Level 2'),
        ('org_level_3', 'Org Level 3'),
        ('business_critical', 'Business Critical'),
        ('iprm_id', 'IPRM Questionnaire ID'),
        ('cpr_type', 'CRP Type'),
        ('compliance_rating_status', 'Compliance Rating Status'),
        ('sdlc_path', 'SDLC Path'),
        ('dr_rto_tier', 'DR/RTO Tier'),
        ('sox_value', 'SOX Value'),
        ('gxp', 'GxP?'),
        ('gcp', 'GCP?'),
        ('gdp', 'GDP?'),
        ('glp', 'GLP?'),
        ('gmp', 'GMP?'),
        ('gpvp', 'GPvP?'),
        ('eea_pi_spi', 'EEA PI/SPI'),
        ('ma201', 'MA 201'),
        ('sales', 'Sales'),
        ('aca', 'ACA'),
        ('smd', 'SMD'),
        ('data_class', 'Data Classification'),
        ('cybersecurity_protection_level', 'Cybersecurity Protection Level'),
        ('access', 'Access?'),
        ('detect', 'Detect?'),
        ('identify', 'Identify?'),
        ('prevent', 'Prevent?'),
        ('response', 'Response?'),
        ('regional', 'Regional'),
        ('globals', 'Global'),
        ('is_auth', 'I&AM Authentication'),
        ('used_in_lab', 'Used in Lab?'),
        ('ci_mgmt_group', 'CI Mgmt Group'),
        ('under_change_mgmt', 'Under Change Mgmt?'),
        ('sla_support_id', 'SLA Support ID'),
        ('primary_url', 'Primary URL'),
        ('key_used_periods', 'Key Use Periods'),
        ('app_externally_accessible', 'Application Externally Accessible'),
        ('externally_hosted_app', 'Externally Hosted Application'),
        ('country_solution_hosted_in', 'Country Solution Hosted In'),
        ('hosting_vendor', 'Hosting Vendor'),
        ('daily_monitoring_site', 'Daily Monitoring of Site'),
        ('cookies_stored', 'Cookies Stored?'),
        ('customer_into_stored', 'Customer Info Stored?'),
    ))

    def __init__(self):
        super().__init__()
        self._parser = CmdbDataFileParser(keys=self.fields.keys())
