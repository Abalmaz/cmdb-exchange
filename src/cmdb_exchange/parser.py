from copy import deepcopy


class Parser:
    def visit(self, node):
        visit_node_name = 'visit_' + type(node).__name__
        try:
            visit_node = getattr(self, visit_node_name, None)
        except:
            raise RuntimeError(
                'No {} method'.format('visit_' + type(node).__name__))
        return visit_node(node)


class FlatDataParser(Parser):

    def __init__(self):
        self._collected_info = {}
        self._collected_list = []
        self.key = ''

    @property
    def result(self):
        if self._collected_list:
            return self._collected_list
        else:
            return [self._collected_info]

    def visit_list(self, node) -> None:
        for item in node:
            self.visit(item)
            self._collected_list.append(deepcopy(self._collected_info))

    def visit_dict(self, node) -> None:
        for key, value in node.items():
            self.key = key
            self.visit(value)

    def visit_int(self, node) -> None:
        self._collected_info[self.key] = node

    def visit_str(self, node) -> None:
        self._collected_info[self.key] = node

    def visit_bool(self, node) -> None:
        self._collected_info[self.key] = node


class EnvironmentUserFileParser:
    result = []
    keys = ['ciid', 'name', 'users']

    def parse(self, data):
        for row in data:
            envs = row.get('environments')
            for env in envs:
                parse_data = self._parse(env)
                self.result.append(parse_data)
        return self.result

    def _parse(self, data):
        return {key: value for key, value in data.items() if key in self.keys}


class MasterUserFileParser:
    result = []
    keys = ['master_ciid', 'application', 'users']

    def parse(self, data):
        for row in data:
            master = self._parse(row)
            self.result.append(master)
        return self.result

    def _parse(self, data):
        return {key: value for key, value in data.items() if key in self.keys}


class CmdbDataFileParser:
    result = []
    keys = ['ciid',
            'master_ciid',
            'application',
            'name',
            'description',
            'status',
            'env_type',
            'app_deployment_type',
            'location',
            'org_level_1',
            'org_level_2',
            'org_level_3',
            'business_critical',
            'iprm_id',
            'cpr_type',
            'compliance_rating_status',
            'sdlc_path',
            'dr_rto_tier',
            'sox_value',
            'gxp',
            'gcp',
            'gdp',
            'glp',
            'gmp',
            'gpvp',
            'eea_pi_spi',
            'ma201',
            'sales',
            'aca',
            'smd',
            'data_class',
            'cybersecurity_protection_level',
            'access',
            'detect',
            'identify',
            'prevent',
            'response',
            'regional',
            'globals',
            'is_auth',
            'used_in_lab',
            'ci_mgmt_group',
            'under_change_mgmt',
            'sla_support_id',
            'primary_url',
            'key_used_periods',
            'app_externally_accessible',
            'externally_hosted_app',
            'country_solution_hosted_in',
            'hosting_vendor',
            'daily_monitoring_site',
            'cookies_stored',
            'customer_into_stored'
            ]

    def parse(self, data):
        for raw in data:
           self._parse_raw(raw)
        return self.result

    def _parse_raw(self, data):
        master = self._parse(data)
        envs = self._parse_envs(data.get('environments'))
        master['environments'] = envs
        self.result.append(master)

    def _parse_envs(self, envs):
        envs_data = []
        for env in envs:
            env_data = self._parse(env)
            env_data.update(self._parse(env.get("risk_profile")))
            env_data.update(self._parse(env.get('security')))
            envs_data.append(env_data)
        return envs_data

    def _parse(self, data):
        return {key: value for key, value in data.items() if key in self.keys}
