import copy

import fileinput
import itertools
import os
from contextlib import contextmanager

from os import listdir
from os.path import join

from typing import Any, Dict, List

from ..cmdb_exchange.formats import registry
from ..cmdb_exchange.parser import FlatDataParser
from ..cmdb_exchange.utils import get_parent_keys, \
    sorted_list_of_dicts_by_key, combine_many_nested_fields


class Importer:
    """ This is a class handling data from files and translate it to a single
    standardized Python data structure object.
    """

    def __init__(self,
                 format: Any,
                 structure: Dict,
                 mapping_column: Dict) -> None:
        """

        :param format: a class object for work with the given file extension
        :type format: Any
        :param structure: a dictionary describing the data structure
                          according to the schema
        :type structure: Dict
        :param mapping_column: mapping column name and place in the structure
        :type mapping_column: Dict
        """
        self.format = format
        self.structure = structure
        self.mapping_column = mapping_column
        self.result = []

    def push(self, steam: Any) -> List:
        headers = self.format.get_column_name(steam)
        data_rows = self.format.get_data(steam)
        struct_data = self.get_data_by_structure(headers, data_rows)
        result = self.get_single_object_from_data(struct_data)
        return result

    def get_single_object_from_data(self, data):
        keys = get_parent_keys(data[0])
        sorted_data = sorted_list_of_dicts_by_key(data, keys)
        visited, result = [], []
        first, second = {}, {}
        for a, b in itertools.combinations(sorted_data, 2):
            if a not in visited and b not in visited:
                first, second = combine_many_nested_fields(a, b)
                if second:
                    result.append(a)
                    visited.append(a)
                else:
                    visited.append(b)

        result.append(second) if second else result.append(first)
        return result

    def get_data_by_structure(self, headers, data_rows):
        result = []
        for row in data_rows:
            template_dict = copy.deepcopy(self.structure)
            i = 0
            while i < len(headers):
                cell = row[i]
                column_name = headers[i]
                key_path = self.mapping_column[column_name]
                command = f"template_dict{key_path}=\"{cell}\""
                exec(command)
                i += 1
            result.append(template_dict)
        return result

    def open_dir(self, path):
        if os.path.isdir(path):
            allfiles = [f for f in listdir(path)
                        if os.path.isfile(join(path, f))]
            join_data = []
            for file in allfiles:
                fullpath = os.path.join(path, file)
                with open(fullpath) as f:
                    data = self.push(f)
                    join_data = join_data + data
        result = self.get_single_object_from_data(join_data)
        return result

    @contextmanager
    def open(self, path, mode='r', newline=''):
        f = fileinput.input(files=path,
                            openhook=fileinput.hook_encoded("utf-8-sig"))
        try:
            yield f
        finally:
            f.close()


class CmdbExchange:
    """

    """

    _builder = None
    _format = None

    def create_importer(self, format: str, builder: Any) -> None:
        self._builder = builder
        self._format = registry.get_format(format)

    def create_exporter(self, format: str) -> None:
        self._format = registry.get_format(format)

    def prepare_data_for_export(self, data):
        parser = FlatDataParser()
        parser.visit(data)
        return parser.result

    def pull(self, filename, data, fieldnames=None):
        flat_data = self.prepare_data_for_export(data)
        if fieldnames is None:
            fieldnames = flat_data[0].keys()
        return self._format.export_set(filename, flat_data, fieldnames)
