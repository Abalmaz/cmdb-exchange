from collections import defaultdict
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
        return self._collected_list or [self._collected_info]

    def visit_list(self, node) -> None:
        for item in node:
            self.visit(item)
            common_row_data = deepcopy(self._collected_info)
            self._collected_list.append(common_row_data)

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


class SchemaKeysParser(Parser):
    keys = []
    list_of_keys = {}
    key = ''

    @property
    def result(self):
        return self.list_of_keys

    def visit_Nested(self, node):
        self.k = self.key
        self.visit(node.nested._declared_fields)

    def visit_dict(self, node):
        for key, value in node.items():
            self.key = key
            self.visit(value)

    def visit_String(self, node):
        self.keys.append(self.key)

    def visit_Boolean(self, node):
        self.keys.append(self.key)

    def visit_Email(self, node):
        self.keys.append(self.key)

    def visit_Url(self, node):
        self.keys.append(self.key)

    def visit_Integer(self, node):
        self.keys.append(self.key)


class EnvironmentUserFileParser:
    result = []

    def __init__(self, keys):
        self.keys = keys

    def parse(self, data):
        for row in data:
            self._parse_row(row)
        return self.result

    def _parse_row(self, data):
        env = self._parse(data)
        users = self._parse_users(data.get('users'))
        env['users'] = users
        self.result.append(env)

    def _parse_users(self, users):
        return [self._parse(user) for user in users]

    def _parse(self, data):
        return {key: value for key, value in data.items() if key in self.keys}


class MasterUserFileParser:
    result = []

    def __init__(self, keys):
        self.keys = keys

    def parse(self, data):
        self._parse_row(data)
        return self.result

    def _parse_row(self, data):
        master = self._parse(data)
        users = self._parse_users(data.get('users'))
        master['users'] = users
        self.result.append(master)

    def _parse_users(self, users):
        return [self._parse(user) for user in users]

    def _parse(self, data):
        return {key: value for key, value in data.items() if key in self.keys}


class CmdbDataFileParser:
    result = []

    def __init__(self, keys):
        self.keys = keys

    def parse(self, data):
        self._parse_row(data)
        return self.result

    def _parse_row(self, data):
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
