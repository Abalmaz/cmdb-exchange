import pytest

from src.cmdb_exchange.default import CmdbItemBuilder
from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.formats import CSVFormat
from src.cmdb_exchange.utils import flatten_data


def test_get_structure(schema):
    actual = CmdbItemBuilder(schema).get_structure()
    expected = {'master_ciid': '',
                'application': '',
                'environments': {'ciid': '',
                                  'deployment_name': '',
                                  'description': '',
                                  'env_type': '',
                                  'risk_profile': {'gxp': '',
                                                   'iprm_id': '',
                                                   'sdlc_path': '',
                                                   'soc_value': ''},
                                  'status': '',
                                  'url': ''}
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


# def test_importer_get_data_by_structure(csv_upload_file,
#                                         schema,
#                                         python_nested_data):
#     importer = CmdbExchange.create_importer(format='csv',
#                                             builder=CmdbItemBuilder(schema))
#     with importer.open(csv_upload_file) as f:
#         headers = importer.format.get_column_name(f)
#         data_rows = importer.format.get_data(f)
#         actual = importer.get_data_by_structure(headers, data_rows)
#     expected = python_nested_data
#     assert actual == expected


# def test_export_with_csv_format(tmpdir, nested_data, schema):
#     file_name = tmpdir.join('file_name.csv')
#     exporter = CmdbExchange.create_exporter(format='csv')
#     exporter.pull(file_name, nested_data)
#     assert exporter.pull(file_name, nested_data) == \
#            CSVFormat.export_set(data=flatten_data(nested_data), filename=file_name,
#                                 fieldnames=['application', 'master_id', 'env_type',
#                                             'name', 'GxP', 'iprm_id',
#                                             'soc_value', 'sdlc_path', 'url',
#                                             'description', 'status', 'id'])
