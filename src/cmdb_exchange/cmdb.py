import copy
import fileinput
from contextlib import contextmanager
from pprint import pprint

from marshmallow import ValidationError

from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.formats import registry
from src.cmdb_exchange.utils import flatten_data


class CmdbExchange:

    @classmethod
    def get_format(cls, format, command=None):
        fmt = registry.get_format(format)
        if command and not hasattr(fmt, command):
            raise UnsupportedFormat(f'Format {format} cannot be exported.')
        return fmt

    @classmethod
    def create_importer(cls, format, build_schema, **kwargs):
        json_struct = build_schema.get_structure()
        mapping_column = build_schema.get_mapping_column()
        fmt = cls.get_format(format)
        return Importer(fmt, json_struct,
                        mapping_column,
                        build_schema.schema)

    @classmethod
    def create_exporter(cls, format, schema=None, many=True, **kwargs):
        fmt = cls.get_format(format)
        return Exporter(format=fmt,
                        schema=schema,
                        many=many,
                        **kwargs)


class Importer:

    def __init__(self, format, structure, mapping_column, schema):
        self.format = format
        self.structure = structure
        self.mapping_column = mapping_column
        self.schema = schema
        self.column_names = list(mapping_column.keys())
        self._num_columns = 0

    @property
    def num_columns(self):
        self._num_columns = len(self.column_names)
        return self._num_columns

    def push(self, steam):
        result = []
        data_rows = self.format.get_data(steam)
        json_row = self.get_json_row(data_rows)
        for i, row in enumerate(json_row):
            try:
                result.append(self.schema.load(row))
            except ValidationError as err:
                print(f"Validation error in row number {i+1}:")
                pprint(err.messages)
        return result

    def get_json_row(self, data_rows):
        json_struct = []
        for row in data_rows:
            json_row = copy.deepcopy(self.structure)
            i = 0
            while i < self.num_columns:
                cell = row[i]
                column_name = self.column_names[i]
                key_path = self.mapping_column[column_name]
                command = f"json_row{key_path}=\"{cell}\""
                exec(command)
                i += 1
            json_struct.append(json_row)
        return json_struct

    @contextmanager
    def open(self, filepath, mode='r', newline=''):
        f = fileinput.input(files=filepath,
                            openhook=fileinput.hook_encoded("utf-8-sig"))
        try:
            yield f
        finally:
            f.close()


class Exporter:
    def __init__(self, format, schema, many):
        self.format = format
        self.schema = schema
        self.many = many

    def export(self, filename, data, fieldnames=None):
        if self.schema:
            serialized_data = self.schema.dump(data, many=self.many)
            data = serialized_data
        flatt_data = flatten_data(data)
        if fieldnames is None:
            fieldnames = flatt_data[0].keys()

        return self.format.export_set(filename, flatt_data, fieldnames)
