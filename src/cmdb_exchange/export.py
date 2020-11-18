from collections import OrderedDict

from src.cmdb_exchange.parser import EnvironmentUserFileParser, \
    FlatDataParser, MasterUserFileParser, CmdbDataFileParser


class DefaultFile:

    @property
    def file_name(self):
        raise NotImplementedError

    @property
    def fields(self):
        raise NotImplementedError

    def get_data(self, data):
        raise NotImplementedError

    def prepare_data(self, data):
        raise NotImplementedError


class EnvironmentUsersFile(DefaultFile):

    file_name = 'ContactExportEnvironment'

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
        self._parser = EnvironmentUserFileParser(keys=self.fields.keys())
        self._flatten = FlatDataParser()

    def get_data(self, data):
        for row in data:
            self._parser.parse(row.get('environments'))
        return self._parser.result

    def prepare_data(self, data):
        nested_data = self.get_data(data)
        for row in nested_data:
            self._flatten.visit(row)
        return self._flatten.result


class MasterUsersFile(DefaultFile):

    file_name = 'ContactExportMaster'

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
        self._parser = MasterUserFileParser(keys=self.fields.keys())
        self._flatten = FlatDataParser()

    def get_data(self, data):
        for row in data:
            self._parser.parse(row)
        return self._parser.result

    def prepare_data(self, data):
        nested_data = self.get_data(data)
        for row in nested_data:
            self._flatten.visit(row)
        return self._flatten.result


class CmdbDataFile(DefaultFile):

    file_name = 'cmdb-download'

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
        self._parser = CmdbDataFileParser(keys=self.fields.keys())
        self._flatten = FlatDataParser()

    def get_data(self, data):
        for row in data:
            self._parser.parse(row)
        return self._parser.result

    def prepare_data(self, data):
        nested_data = self.get_data(data)
        for row in nested_data:
            self._flatten.visit(row)
        return self._flatten.result

