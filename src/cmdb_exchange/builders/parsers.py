import dataclasses
from collections import defaultdict
from copy import deepcopy
from typing import Any, Union, List

from src.cmdb_exchange.models import Environment, CmdbItem, Security, \
    RiskProfile, Person


class Parser:
    def visit(self, node: Any) -> Any:
        visit_node_name = 'visit_' + type(node).__name__
        try:
            visit_node = getattr(self, visit_node_name, None)
        except:
            raise RuntimeError(
                'No {} method'.format('visit_' + type(node).__name__))
        return visit_node(node)


class FlatDataParser(Parser):
    """
    Flattens a dictionary with nested structure to a dictionary with no
    hierarchy
    """

    def __init__(self):
        self._collected_info = {}
        self._collected_list = []
        self.key = ''

    @property
    def result(self) -> Union[list, List[dict]]:
        return self._collected_list or [self._collected_info]

    def visit_list(self, node: list) -> None:
        for item in node:
            self.visit(item)
            common_row_data = deepcopy(self._collected_info)
            self._collected_list.append(common_row_data)

    def visit_dict(self, node: dict) -> None:
        for key, value in node.items():
            self.key = key
            self.visit(value)

    def visit_int(self, node: int) -> None:
        self._collected_info[self.key] = node

    def visit_str(self, node: str) -> None:
        self._collected_info[self.key] = node

    def visit_bool(self, node: bool) -> None:
        self._collected_info[self.key] = node


class BaseFileParser:
    """
    The base class specifies methods for read/write file
    """

    def import_data(self, data):
        """
        Parses data read from a file and creates necessary python objects from them.
        """
        raise NotImplementedError

    def _export_row(self, data):
        """
        Parses dictionary with cmdb item data, and get from it needed data to create file
        :param data:
        :return:
        """
        raise NotImplementedError

    def export_data(self, data: list) -> list:
        """
        Reads a given list of cmdb item objects by one and prepare it to export
        :param data:
        :return:
        """
        result = []
        for row in data:
            result.append(self._export_row(row))
        return result

    @staticmethod
    def _parse(data: dict, keys: list) -> dict:
        """
        Returns a new dictionary contain only certain keys.

        :param data: dict. Dict that has a whole bunch of entries
        :param keys: list. List of keys for filtering
        :return: dict
        """
        return {key: value for key, value in data.items() if key in keys}


class ContactFileParser(BaseFileParser):

    def __init__(self, keys):
        self.keys = keys

    def _export_row(self, data: dict) -> dict:
        parent = self._parse(data, self.keys)
        users = [self._parse_user(user) for user in data.get('users')]
        parent['users'] = users
        return parent

    def _parse_user(self, data: dict) -> dict:
        user_data = self._parse(data, Person.get_keys())
        if user_data:
            user = Person(**user_data)
            return dataclasses.asdict(user)

    def import_data(self, data: list) -> defaultdict:
        result = defaultdict(list)
        for row in data:
            user = self._parse_user(row)
            parent = row.get('ciid' if 'ciid' in row else 'master_ciid')
            result[parent].append(user)
        return result


class CmdbDataFileParser(BaseFileParser):

    def __init__(self, keys):
        self.keys = keys

    def _export_row(self, data: dict) -> dict:
        master = self._parse(data, self.keys)
        envs = [self._export_env(env) for env in data.get('environments')]
        master['environments'] = envs
        return master

    def _export_env(self, env: dict) -> dict:
        env_data = self._parse(env, self.keys)
        risk_profile = env.get("risk_profile")
        security = env.get('security')
        if risk_profile:
            env_data.update(self._parse(risk_profile, self.keys))
        if security:
            env_data.update(self._parse(security, self.keys))
        return env_data

    def _parse_master(self, data: list) -> List[dict]:
        masters = []
        for row in data:
            master_data = self._parse(row, CmdbItem.get_keys())
            masters.append(master_data)
        return [dict(t) for t in {tuple(d.items())for d in masters}]

    def _parse_envs(self, data: list) -> defaultdict:
        result = defaultdict(list)
        for row in data:
            env = self._parse_env(row)
            master_id = row.get('master_ciid')
            result[master_id].append(env)
        return result

    def _parse_env(self, data: dict) -> dict:
        risk_profile_data = self._parse_risk_profile(data)
        security_data = self._parse_security(data)
        env_data = self._parse(data, Environment.get_keys())
        env = Environment(**env_data,
                          risk_profile=risk_profile_data,
                          security=security_data)
        return dataclasses.asdict(env)

    def _parse_risk_profile(self, data: dict) -> [RiskProfile, None]:
        risk_profile_data = self._parse(data, RiskProfile.get_keys())
        if not risk_profile_data.get('iprm_id'):
            return None
        return RiskProfile(**risk_profile_data)

    def _parse_security(self, data: dict) -> [Security, None]:
        security_data = self._parse(data, Security.get_keys())
        if not any(security_data.values()):
            return None
        return Security(**security_data)

    def import_data(self, data: list) -> List[dict]:
        envs_data = self._parse_envs(data)
        cmdb_items = self._parse_master(data)
        for cmdb_item in cmdb_items:
            cmdb_item['environments'] = envs_data.get(cmdb_item['master_ciid'])
        return cmdb_items
