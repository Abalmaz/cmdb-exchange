import pytest

from src.cmdb_exchange.builders import EnvironmentUsersBuilder, MasterUsersBuilder, \
    CmdbDataBuilder
from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.exceptions import UnsupportedFormat, NotExistingBuilder


def test_create_exporter_with_unknown_format():
    with pytest.raises(UnsupportedFormat) as error:
        CmdbExchange.create_exporter('zzz', EnvironmentUsersBuilder())
    exception_msg = error.value.args[0]
    assert exception_msg == "The 'zzz' format is not available."


class TestBuilder:
    pass


def test_create_exporter_with_unknown_builder():
    with pytest.raises(NotExistingBuilder) as error:
        CmdbExchange.create_exporter('csv', TestBuilder())
    exception_msg = error.value.args[0]
    assert exception_msg == "The 'TestBuilder' builder does not exist."


def test_create_environment_users_file(tmpdir,
                                        python_nested_data,
                                        environment_users_csv_file):
    exporter = CmdbExchange.create_exporter('csv', EnvironmentUsersBuilder())
    exporter.export(tmpdir, python_nested_data)
    file_name = tmpdir.join('ContactExportEnvironment.csv')
    assert file_name.read() == environment_users_csv_file.read()


def test_create_master_users_file(tmpdir,
                                  python_nested_data,
                                  master_users_csv_file):
    exporter = CmdbExchange.create_exporter('csv', MasterUsersBuilder())
    exporter.export(tmpdir, python_nested_data)
    file_name = tmpdir.join('ContactExportMaster.csv')
    assert file_name.read() == master_users_csv_file.read()


def test_create_cmdb_download_file(tmpdir,
                                  python_nested_data,
                                  cmdb_data_csv_file):
    exporter = CmdbExchange.create_exporter('csv', CmdbDataBuilder())
    exporter.export(tmpdir, python_nested_data)
    file_name = tmpdir.join('cmdb-download.csv')
    assert file_name.read() == cmdb_data_csv_file.read()

