import copy

import fileinput
import itertools
import os
from contextlib import contextmanager

from os import listdir
from os.path import join

from typing import Any, Dict, List

from ..cmdb_exchange.formats import registry
from ..cmdb_exchange.utils import get_parent_keys, \
    sorted_list_of_dicts_by_key, combine_many_nested_fields


class Importer:
    """ This is a class handling data from files and translate it to a single
    standardized Python data structure object.
    """

    def __init__(self, format, builder):
        self._format = format
        self._builder = builder

    def push(self, steam: Any) -> List:
        data_rows = self._format.import_set(steam)
        result = self._builder.get_data(data_rows)
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


class Exporter:
    def __init__(self, format, builder):
        self._format = format
        self._builder = builder

    def export(self, path,  data):
        data_for_export = self._builder.prepare_data(data)
        file_name = path + self._builder.file_name + '.'+self._format.title
        self._format.export_set(filename=file_name,
                                data=data_for_export,
                                fieldnames=self._builder.fields.keys(),
                                headers=self._builder.fields)


class CmdbExchange:
    """

    """

    @classmethod
    def create_importer(cls, format: str, builder: Any) -> object:
        return Importer(format=registry.get_format(format),
                        builder=builder)

    @classmethod
    def create_exporter(cls, format: str, builder: Any) -> object:
        return Exporter(format=registry.get_format(format),
                        builder=builder)
