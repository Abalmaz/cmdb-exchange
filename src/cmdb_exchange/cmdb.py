from typing import Any, Union, List

from .builders import builders
from .utils import get_file_by_name_pattern
from ..cmdb_exchange.formats import registry


class Importer:
    """ This is a class handling data from files and translate it to a single
    standardized Python data structure object.
    """

    def __init__(self, schema: Any, fmt: Any) -> None:
        self._schema = schema
        self._format = fmt

    def get_data(self, obj_key: str, path: str) -> Union[dict, List[dict]]:
        builder = builders.get_builder(obj_key)
        file_name = f'{builder.file_name}.{self._format.title}'
        file = get_file_by_name_pattern(path, file_name)
        file_data = self.read_file(file)
        return builder.import_data(file_data)

    def import_data(self, path: str) -> list:
        master_users_data = self.get_data('master_contacts', path)
        env_users_data = self.get_data('env_contacts', path)
        cmdb_data = self.get_data('cmdb_items', path)
        for item in cmdb_data:
            item['users'] = master_users_data.get(item['master_ciid'])
            for env in item['environments']:
                env['users'] = env_users_data.get(env['ciid'])
            print(item)
            serialize_item = self._schema.load(item)
            print(serialize_item)
        # serialize = self._schema.load(cmdb_data)
        # print(serialize)
        return cmdb_data

    def read_file(self, path: str) -> list:
        with open(path) as f:
            read_file = self._format.get_data(f)
        return read_file


class Exporter:
    """

    """

    def __init__(self, fmt: Any, builder: Any) -> None:
        self._format = fmt
        self._builder = builder

    def get_file_name(self, path: str) -> str:
        return f'{path}/{self._builder.generate_filename()}.{self._format.title}'

    def export(self, path: str,  data: Any) -> None:
        data_for_export = self._builder.export_data(data)
        file_name = self.get_file_name(path)
        self._format.create_file(filename=file_name,
                                 data=data_for_export,
                                 fieldnames=self._builder.fields.keys(),
                                 headers=self._builder.fields)


class CmdbExchange:
    """

    """

    @classmethod
    def create_importer(cls, fmt: str, schema: Any) -> Importer:
        return Importer(fmt=registry.get_format(fmt),
                        schema=schema)

    @classmethod
    def create_exporter(cls, fmt: str, builder: Any) -> Exporter:
        return Exporter(fmt=registry.get_format(fmt),
                        builder=builder)
