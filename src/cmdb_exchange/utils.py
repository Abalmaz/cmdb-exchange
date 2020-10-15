from copy import deepcopy
from typing import Any, Generator, Iterable, List


def cross_join(left: Iterable,
               right: Iterable) -> List:
    new_rows = []
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data: Iterable) -> Generator[Any, Any, None]:
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def flatten_data(data: Any, key: str = '') -> Any:
    if isinstance(data, dict):
        rows = [{}]
        for key, value in data.items():
            rows = cross_join(rows, flatten_data(
                value, key)
                              )
    elif isinstance(data, list):
        rows = []
        for i in range(len(data)):
            [rows.append(elem) for elem in flatten_list(
                flatten_data(data[i])
            )]
    else:
        rows = [{key: data}]
    return rows
