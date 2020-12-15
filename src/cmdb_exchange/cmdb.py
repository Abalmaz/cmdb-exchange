from typing import Any, Union, List

from .builders import builders
from .utils import get_file_by_name_pattern
from ..cmdb_exchange.formats import registry


class Importer:
    """ This class provides an interface for realize import data from files
    and translate it to a single standardized Python data structure object.
    """

    def __init__(self, schema: Any, fmt: Any) -> None:
        self._schema = schema
        self._format = fmt

    def get_data(self, obj_key: str, path: str) -> Union[dict, List[dict]]:
        """
        The main method implements the data import process. It generates a fully qualified
        filename using the name from the given builder and the extension from the given format.
        After that, it looks for a file in the folder. If the file was found, read it and return the data.

        :param obj_key: str. The key with which our builder is registered in RegistryBuilders class.
        :param path: The path to the folder in which the file we need is located.
        :return: Union[dict, List[dict]] Data from file
        """
        builder = builders.get_builder(obj_key)
        file_name = f'{builder.file_name}.{self._format.title}'
        file = get_file_by_name_pattern(path, file_name)
        file_data = self.read_file(file)
        return builder.import_data(file_data)

    def create_objects_from_files(self, path: str) -> list:
        """
        Calls the get_data method for all files containing data in turn
        and combines all received data from all files into one common list of objects

        :param path: The path to the folder in which the file we need is located.
        :return: list. List of cmdb item objects
        """
        master_users_data = self.get_data('master_contacts', path)
        env_users_data = self.get_data('env_contacts', path)
        cmdb_data = self.get_data('cmdb_items', path)
        for item in cmdb_data:
            item['users'] = master_users_data.get(item['master_ciid'])
            for env in item['environments']:
                env['users'] = env_users_data.get(env['ciid'])
        return cmdb_data

    def import_data(self, path: str) -> list:
        """
        Calls method for getting data from files and serialized it.

        :param path: The path to the folder in which the file we need is located.
        :return: list. List of serialized cmdb item objects
        """
        serialize_data = []
        cmdb_data = self.create_objects_from_files(path)
        for item in cmdb_data:
            serialize_data.append(self._schema.load(item))
        return serialize_data

    def read_file(self, path: str) -> list:
        with open(path) as f:
            read_file = self._format.get_data(f)
        return read_file


class Exporter:
    """
    This class provides interface for realize export a standardized
    Python data structure to a to a file with given extension
    and using given builder.
    """

    def __init__(self, fmt: Any, builder: Any) -> None:
        self._format = fmt
        self._builder = builder

    def get_file_name(self, path: str) -> str:
        return f'{path}/{self._builder.generate_filename()}.{self._format.title}'

    def export(self, path: str,  data: list) -> None:
        """
        The main method which creates a file with data and saves it in a given folder.

        :param path: str. Folder's path for saving created files
        :param data: list. List of CMDB item dictionaries.
        :return:
        """
        data_for_export = self._builder.export_data(data)
        file_name = self.get_file_name(path)
        self._format.create_file(filename=file_name,
                                 data=data_for_export,
                                 fieldnames=self._builder.fields.keys(),
                                 headers=self._builder.fields)


class CmdbExchange:
    """
    The class provides a simple interface for work with the library.
    """

    @classmethod
    def create_importer(cls, fmt: str, schema: Any) -> Importer:
        """
        Gets format class by given key and creates instance
        of class Importer with given parameters.

        :param fmt: str. Extension of files used for import data
        :param schema: Any. The schema used for serialization/deserialization of data
        :return: Importer
        """
        return Importer(fmt=registry.get_format(fmt),
                        schema=schema)

    @classmethod
    def create_exporter(cls, fmt: str, builder: Any) -> Exporter:
        """
        Method returns instance of Exporter class witch realize export given data to file

        :param fmt: str. Extension of files used for export data
        :param builder: Any. File builder for creates file
        :return: Exporter
        """
        return Exporter(fmt=registry.get_format(fmt),
                        builder=builder)
