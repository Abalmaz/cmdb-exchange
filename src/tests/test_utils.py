import pytest

from src.cmdb_exchange.utils import flatten_data, get_parent_keys, \
    sorted_list_of_dicts_by_key, is_dict_has_value, combine_many_nested_fields


def test_flatten_data(nested_data):
    flatted_data = [
        {'master_id': 123, 'id': 111, 'name': 'Web Server', 'status': 'Run',
         'GxP': True},
        {'master_id': 123, 'id': 112, 'name': 'Web Server', 'status': 'New',
         'GxP': True},
        {'master_id': 123, 'id': 113, 'name': 'Web Server', 'status': 'Run',
         'GxP': False},
        {'master_id': 456, 'id': 211, 'name': 'Mobile app', 'status': 'Build',
         'GxP': True},
        {'master_id': 456, 'id': 212, 'name': 'Mobile app', 'status': 'Run',
         'GxP': True},
        {'master_id': 456, 'id': 213, 'name': 'Mobile app', 'status': 'Run',
         'GxP': True}
    ]
    assert flatted_data == flatten_data(nested_data)


def test_get_parent_key(python_nested_data):
    actual = get_parent_keys(python_nested_data[0])
    expected = ['application', 'master_ciid']
    assert actual == expected


def test_sorted_list_of_dicts_by_key(python_nested_data):
    actual = sorted_list_of_dicts_by_key(python_nested_data,
                                         ['application', 'master_ciid'])
    expected = [
        {'application': 'EXTERNAL WEBSITE: QUITWITHHELP',
         'environments': {'ciid': 'SC2747583',
                          'deployment_name': 'EXTERNAL WEBSITE: QUITWITHHELP '
                                             '(BIOPHARMA)',
                          'description': 'External website',
                          'env_type': 'Prodaction',
                          'risk_profile': {'gxp': 'True',
                                           'iprm_id': '3275727',
                                           'sdlc_path': 'Baseline',
                                           'soc_value': 'True'},
                          'status': 'Run',
                          'url': 'arreterdefumeravecaide.be'},
         'master_ciid': 'SC2465284'},
        {'application': 'PRODUCT WEBSITE: CALTRATE',
         'environments': {'ciid': 'SC2550040',
                          'deployment_name': "PRODUCT WEBSITE: CALTRATE (CONSUMER)'",
                          'description': 'CALTRATE.COM IS TRANSITIIOND TO DRUPAL '
                                         'PLATFORM, HOSTED EXTERNALLY BY VERIZON',
                          'env_type': 'Staging',
                          'risk_profile': {'gxp': 'True',
                                           'iprm_id': '3275727',
                                           'sdlc_path': 'Baseline',
                                           'soc_value': 'True'},
                          'status': 'Run',
                          'url': 'http://stg.caltrate.pfizer.com'},
         'master_ciid': 'SC2265886'},
        {'application': 'PRODUCT WEBSITE: CALTRATE',
         'environments': {'ciid': 'SC2630860',
                          'deployment_name': 'PRODUCT WEBSITE: WEBINARS (DIGITAL)',
                          'description': 'New website for Webinars',
                          'env_type': 'Development',
                          'risk_profile': {'gxp': 'True',
                                           'iprm_id': '3275727',
                                           'sdlc_path': 'Baseline',
                                           'soc_value': 'True'},
                          'status': 'New',
                          'url': 'webinar'},
         'master_ciid': 'SC2265886'}
    ]
    assert actual == expected


empty_dict_for_test = [
    {'': ''},
    {'id': '', 'name': ''},
    {'id': '', 'environments': {'id': '', 'name': ''}},
    {'id': '', 'environments': [{'id': '', 'name': ''},
                                {'id': '', 'name': ''}]}
]

empty_dict_ids = [f'{t}' for t in empty_dict_for_test]


@pytest.mark.parametrize('empty_dict', empty_dict_for_test, ids=empty_dict_ids)
def test_is_dict_has_value(empty_dict):
    actual = is_dict_has_value(empty_dict)
    assert actual == False


dict_with_data_for_test = [
    {'': '1'},
    {'id': '', 'name': 'test'},
    {'id': '', 'environments': {'id': '', 'name': 'test'}},
    {'id': '', 'environments': [{'id': '', 'name': ''},
                                {'id': '', 'name': 'test'}]}
]

dict_ids = [f'{t}' for t in dict_with_data_for_test]


@pytest.mark.parametrize('data_dict', dict_with_data_for_test, ids=dict_ids)
def test_is_dict_has_value_true(data_dict):
    actual = is_dict_has_value(data_dict)
    assert actual == True


def test_combine_row_related_rows():
    row1 = {'id': 1, 'name': 'test', 'envs': [{'id': 11, 'status': 'run'}]}
    row2 = {'id': 1, 'name': 'test', 'envs': [{'id': 12, 'status': 'build'}]}
    actual1, actual2 = combine_many_nested_fields(row1, row2)
    expected1 = {'id': 1, 'name': 'test', 'envs': [{'id': 11, 'status': 'run'},
                                                   {'id': 12, 'status': 'build'}
                                                   ]}
    expected2 = {}
    assert actual1 == expected1
    assert actual2 == expected2


def test_combine_row_not_related_rows():
    row1 = {'id': 1, 'name': 'test', 'envs': [{'id': 11, 'status': 'run'}]}
    row2 = {'id': 2, 'name': 'test2', 'envs': [{'id': 12, 'status': 'build'}]}
    actual1, actual2 = combine_many_nested_fields(row1, row2)
    expected1 = {'id': 1, 'name': 'test', 'envs': [{'id': 11, 'status': 'run'}]}
    expected2 = {'id': 2, 'name': 'test2', 'envs': [{'id': 12, 'status': 'build'}]}
    assert actual1 == expected1
    assert actual2 == expected2