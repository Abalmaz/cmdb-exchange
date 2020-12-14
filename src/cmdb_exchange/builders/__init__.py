from src.cmdb_exchange.builders.builders import EnvironmentUsersBuilder, \
    MasterUsersBuilder, CmdbDataBuilder
from src.cmdb_exchange.exceptions import NotExistingBuilder


class RegistryBuilders:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def get_builder(self, key):
        builder = self._builders.get(key)
        if not builder:
            raise NotExistingBuilder(f"The '{key}' builder does not exist.")
        return builder


builders = RegistryBuilders()
builders.register_builder('env_contacts', EnvironmentUsersBuilder())
builders.register_builder('master_contacts', MasterUsersBuilder())
builders.register_builder('cmdb_items', CmdbDataBuilder())
