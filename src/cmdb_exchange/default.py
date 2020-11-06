from marshmallow.fields import Nested


class CmdbItemBuilder:

    def __init__(self, schema):
        self.schema = schema

    def get_structure(self):
        return self.generate_data_structure(self.schema)

    def get_mapping_column(self):
        return self.get_leaves(self.schema)

    def generate_data_structure(self, schema):
        schema = schema._declared_fields
        column_names = list(schema.keys())
        visited = set()
        structure = {}
        for l1 in column_names:
            if l1 not in visited:
                structure[l1] = ''
            if type(schema[l1]) is Nested:
                nodes = {}
                nested_schema = schema[l1].nested._declared_fields
                l2_column_name = list(nested_schema.keys())
                for l2 in l2_column_name:
                    if l2 not in visited:
                        nodes[l2] = ''
                        visited.add(l2)
                    if type(nested_schema[l2]) is Nested:
                        nodes[l2] = self.generate_data_structure(nested_schema[l2].nested)
                        visited.add(l2)
                    if len(visited) == len(l2_column_name):
                        structure[l1] = [nodes] if schema[l1].many else nodes
        return structure

    def get_leaves(self, schema, path="", result={}):
        for key, value in schema._declared_fields.items():
            if type(value) is Nested:
                if schema._declared_fields[key].many:
                    self.get_leaves(value.nested, f"{path}['{key}'][0]", result)
                else:
                    self.get_leaves(value.nested, f"{path}['{key}']", result)
            else:
                if key in result:
                    parent_name = path.replace('[', '').replace("'", '').split("]")
                    new_key = f"{parent_name[0]}_{key}"
                    result[new_key] = f"{path}['{key}']"
                else:
                    result[key] = f"{path}['{key}']"
        return result
