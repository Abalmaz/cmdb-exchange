import copy

from marshmallow.fields import Nested


class CmdbItemBuilder:
    def __init__(self, schema):
        self.schema = schema
        self.delimiters = "."

    def populate_structure_with_data(self, structure, column_names, data_rows):
        json_struct = []
        num_columns = len(column_names)
        mapping = self.get_leaves(self.schema)
        for row in data_rows:
            json_row = copy.deepcopy(structure)
            i = 0
            while i < num_columns:
                cell = row[i]
                column_name = column_names[i]
                key_path = mapping[column_name]
                command = f"json_row{key_path}=\"{cell}\""
                exec(command)
                i += 1
            json_struct.append(json_row)
        return json_struct

    def generate_json_structure(self, schema):
        schema = schema._declared_fields
        column_names = list(schema.keys())
        visited = set()
        structure = {}
        for l1 in column_names:
            if l1 not in visited:
                structure[l1] = l1
            if type(schema[l1]) is Nested:
                nodes = {}
                nested_schema = schema[l1].nested._declared_fields
                l2_column_name = list(nested_schema.keys())
                for l2 in l2_column_name:
                    if l2 not in visited:
                        nodes[l2] = l2
                        visited.add(l2)
                    if type(nested_schema[l2]) is Nested:
                        nodes[l2] = self.generate_json_structure(nested_schema[l2].nested)
                        visited.add(l2)
                    if len(visited) == len(l2_column_name):
                        structure[l1] = nodes
        return structure

    def get_leaves(self, schema, path="", result={}):
        for k, v in schema._declared_fields.items():
            if type(v) is Nested:
                self.get_leaves(v.nested, f"{path}['{k}']", result)
            else:
                result[k] = f"{path}['{k}']"
        return result
