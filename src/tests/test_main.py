import pytest

from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.formats.csv import CSVFormat
from src.cmdb_exchange.main import get_extension, CmdbExchange
from src.cmdb_exchange.utils import flatten_data


def test_flatten_data(nested_data):
    flatted_data = [
        {'master_id': 123, 'id': 111, 'name': 'Web Server', 'status': 'Run', 'GxP': True},
        {'master_id': 123, 'id': 112, 'name': 'Web Server', 'status': 'New', 'GxP': True},
        {'master_id': 123, 'id': 113, 'name': 'Web Server', 'status': 'Run', 'GxP': False},
        {'master_id': 456, 'id': 211, 'name': 'Mobile app', 'status': 'Build', 'GxP': True},
        {'master_id': 456, 'id': 212, 'name': 'Mobile app', 'status': 'Run', 'GxP': True},
        {'master_id': 456, 'id': 213, 'name': 'Mobile app', 'status': 'Run', 'GxP': True}
    ]
    assert flatted_data == flatten_data(nested_data)


def test_get_unknown_format():
    with pytest.raises(UnsupportedFormat) as error:
        get_extension(filename="???.???")
    exception_msg = error.value.args[0]
    assert exception_msg == "Format ??? cannot be exported."


def test_get_csv_format():
    assert get_extension(filename="test.csv") == CSVFormat


def test_transfer_csv_load(nested_data):
    assert CmdbExchange.export(data=nested_data, filename='test.csv') == \
           CSVFormat.export_set(data=nested_data, filename='test.csv')
