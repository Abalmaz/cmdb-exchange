from src.cmdb_exchange.export import CmdbDataFile


class Builder:
    pass


class CmbdItemBuilder(Builder):

    result = []

    def __init__(self, schema):
        self._schema = schema
        self._file_parser = CmdbDataFile()

    # TODO:
    def set_correct_keys(self, data):
        new_row = {}
        new_data = []
        for row in data:
            for k, v in self._file_parser.fields.items():
                for row_k, row_v in row.items():
                    if row_k == v:
                        new_row[k] = row_v
            new_data.append(new_row)
        return new_data

    def get_data(self, data):
        self.parse(data)
        # print(self.result)
        # for row in self.result:
        #     print(row)
        #     self._schema.load(row)

        return self.result

    def parse(self, data):
        updated_key_data = self.set_correct_keys(data)
        for row in updated_key_data:
            self._parse_row(row)

    def _parse_row(self, data):
        master = self._parse_master(data)
        envs = self._parse_envs(data)
        parent = self.check_parents(master)
        if parent:
            parent['environments'].append(envs)
        else:
            master['environments'] = [envs]
            self.result.append(master)

    def _parse_master(self, data):
        master_keys = self._schema.declared_fields.keys()
        master_data = self._parse(data, master_keys)
        master = self._schema.load(master_data)
        return master

    def _parse_envs(self, envs):
        env_fields = self._schema.declared_fields['environments'].nested._declared_fields
        env_keys = env_fields.keys()
        risk_profile_keys = env_fields['risk_profile'].nested._declared_fields.keys()
        security_keys = env_fields['security'].nested._declared_fields.keys()
        env_data = self._parse(envs, env_keys)
        risk_profile = self._parse(envs, risk_profile_keys)
        security = self._parse(envs, security_keys)
        env_data['risk_profile'] = risk_profile
        env_data['security'] = security
        return env_data

    def _parse(self, data, keys):
        return {key: value for key, value in data.items() if key in keys}

    def check_parents(self, row):
        for i, item in enumerate(self.result):
            if item['master_ciid'] == row['master_ciid']:
                return item
        return None
