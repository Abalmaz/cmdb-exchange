import operator
from typing import List, Tuple, Dict


def get_parent_keys(data: Dict) -> List:
    parent_key = []
    for key, value in data.items():
        if not isinstance(value, (list, dict)):
            parent_key.append(key)
    return parent_key


def sorted_list_of_dicts_by_key(data: List, keys: List) -> List:
    return sorted(data, key=operator.itemgetter(*keys))


def is_dict_has_value(some_dict: Dict) -> bool:
    result = False
    for value in some_dict.values():
        if isinstance(value, str) and value != '':
            result = True
        if isinstance(value, Dict):
            result = is_dict_has_value(value)
        if isinstance(value, List):
            for item in value:
                result = is_dict_has_value(item)
    return result


def combine_many_nested_fields(first_row: Dict,
                               second_row: Dict) -> Tuple[Dict, Dict]:
    parent_fields_first_row, parent_fields_second_row = {}, {}
    is_combine = False
    parent_keys = get_parent_keys(second_row)
    for key in parent_keys:
        parent_fields_first_row[key] = first_row[key]
        parent_fields_second_row[key] = second_row[key]
    for key, value in second_row.items():
        if isinstance(value, list):
            many_field = key
            if parent_fields_first_row == parent_fields_second_row:
                for item in second_row[many_field]:
                    if is_dict_has_value(item):
                        first_row[many_field].append(item)
                        is_combine = True
            if len(first_row[key]) > 1:
                for item in first_row[many_field]:
                    if not is_dict_has_value(item):
                        first_row[many_field].remove(item)
    if is_combine:
        second_row = {}
    return first_row, second_row
