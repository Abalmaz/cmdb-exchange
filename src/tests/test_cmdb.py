import pytest

from src.cmdb_exchange.default import CmdbItemBuilder
from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.formats import CSVFormat
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


def test_get_wrong_format():
    with pytest.raises(UnsupportedFormat):
        CmdbExchange.get_format('aaa')


def test_get_structure(schema):
    actual = CmdbItemBuilder(schema).get_structure()
    expected = {'master_ciid': 'master_ciid',
                'application': 'application',
                'environments': {'ciid': 'ciid',
                                  'deployment_name': 'deployment_name',
                                  'description': 'description',
                                  'env_type': 'env_type',
                                  'risk_profile': {'gxp': 'gxp',
                                                   'iprm_id': 'iprm_id',
                                                   'sdlc_path': 'sdlc_path',
                                                   'soc_value': 'soc_value'},
                                  'status': 'status',
                                  'url': 'url'}
                }
    assert actual == expected


def test_get_mapping_column(schema):
    actual = CmdbItemBuilder(schema).get_mapping_column()
    expected = {'application': "['application']",
                 'ciid': "['environments']['ciid']",
                 'deployment_name': "['environments']['deployment_name']",
                 'description': "['environments']['description']",
                 'env_type': "['environments']['env_type']",
                 'gxp': "['environments']['risk_profile']['gxp']",
                 'iprm_id': "['environments']['risk_profile']['iprm_id']",
                 'master_ciid': "['master_ciid']",
                 'sdlc_path': "['environments']['risk_profile']['sdlc_path']",
                 'soc_value': "['environments']['risk_profile']['soc_value']",
                 'status': "['environments']['status']",
                 'url': "['environments']['url']"}
    assert actual == expected


def test_importer_get_json_row(csv_upload_file, schema, python_nested_data):
    importer = CmdbExchange.create_importer('csv', CmdbItemBuilder(schema))
    with importer.open(csv_upload_file) as f:
        data_rows = importer.format.get_data(f)
        actual = importer.get_json_row(data_rows)
    expected = python_nested_data
    assert actual == expected


def test_export_with_csv_format(tmpdir, nested_data, schema):
    file_name = tmpdir.join('file_name.csv')
    exporter = CmdbExchange.create_exporter('csv', schema)
    exporter.export(file_name, nested_data)
    assert exporter.export(file_name, nested_data) == \
           CSVFormat.export_set(data=flatten_data(nested_data), filename=file_name,
                                fieldnames=['application', 'master_id', 'env_type',
                                            'name', 'GxP', 'iprm_id',
                                            'soc_value', 'sdlc_path', 'url',
                                            'description', 'status', 'id'])
