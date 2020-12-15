import os

import pytest
from freezegun import freeze_time

from src.cmdb_exchange.builders import EnvironmentUsersBuilder, MasterUsersBuilder, CmdbDataBuilder
from src.cmdb_exchange.builders.parsers import FlatDataParser
from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.schemas import MasterSchema


def test_unknown_format():
    with pytest.raises(UnsupportedFormat) as error:
        CmdbExchange.create_exporter('zzz', EnvironmentUsersBuilder())
    exception_msg = error.value.args[0]
    assert exception_msg == "The 'zzz' format is not available."


@freeze_time("2020-12-10")
def test_create_csv_environment_users_file(tmpdir,
                                           python_nested_data,
                                           environment_users_csv_file):
    exporter = CmdbExchange.create_exporter('csv', EnvironmentUsersBuilder())
    exporter.export(tmpdir, python_nested_data)
    file_name = tmpdir.join('AppSearchContactExport_20201210_Environment.csv')
    assert file_name.read() == environment_users_csv_file.read()


@freeze_time("2020-12-10")
def test_create_csv_master_users_file(tmpdir,
                                      python_nested_data,
                                      master_users_csv_file):
    exporter = CmdbExchange.create_exporter('csv', MasterUsersBuilder())
    exporter.export(tmpdir, python_nested_data)
    file_name = tmpdir.join('AppSearchContactExport_20201210_Master.csv')
    assert file_name.read() == master_users_csv_file.read()


def test_create_csv_cmdb_download_file(tmpdir,
                                       python_nested_data,
                                       cmdb_data_csv_file):
    exporter = CmdbExchange.create_exporter('csv', CmdbDataBuilder())
    exporter.export(tmpdir, python_nested_data)
    file_name = tmpdir.join('cmdb-sample-download.csv')
    assert file_name.read() == cmdb_data_csv_file.read()


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'AppSearchContactExport_20201210_Environment.csv'),
    os.path.join(FIXTURE_DIR, 'AppSearchContactExport_20201210_Master.csv'),
    os.path.join(FIXTURE_DIR, 'cmdb-sample-download.csv'),
    )
def test_importer(datafiles, python_nested_data):
    path = str(datafiles)
    importer = CmdbExchange.create_importer('csv', MasterSchema())
    data = importer.import_data(path)
    assert data == python_nested_data


def test_flatt_parser():
    nested_data = {
        'master_id': 123,
        'environments': [
            {'id': 111, 'name': 'Web Server', 'status': 'Run',
             'risk_profile_data': {'GxP': True}},
            {'id': 112, 'name': 'Web Server', 'status': 'New',
             'risk_profile_data': {'GxP': True}},
            {'id': 113, 'name': 'Web Server', 'status': 'Run',
             'risk_profile_data': {'GxP': False}}
        ]
    }
    parser = FlatDataParser()
    expected = [{'master_id': 123, 'id': 111, 'name': 'Web Server', 'status': 'Run', 'GxP': True},
                {'master_id': 123, 'id': 112, 'name': 'Web Server', 'status': 'New', 'GxP': True},
                {'master_id': 123, 'id': 113, 'name': 'Web Server', 'status': 'Run', 'GxP': False}
                ]
    parser.visit(nested_data)
    actual = parser.result
    assert actual == expected
