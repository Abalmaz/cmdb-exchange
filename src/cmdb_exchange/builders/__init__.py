from src.cmdb_exchange.builders.export import EnvironmentUsersFile, \
    MasterUsersFile, CmdbDataFile
from src.cmdb_exchange.exceptions import NotExistingBuilder


class RegistryBuilders:
    def __init__(self):
        self._builders = {}

    def register_builder(self, builder):
        key = builder.__class__.__name__
        self._builders[key] = builder

    def get_builder(self, builder, **kwargs):
        key = builder.__class__.__name__
        bld = self._builders.get(key)
        if not bld:
            raise NotExistingBuilder(f"The '{key}' builder does not exist.")
        return bld


builders = RegistryBuilders()
builders.register_builder(EnvironmentUsersFile())
builders.register_builder(MasterUsersFile())
builders.register_builder(CmdbDataFile())
