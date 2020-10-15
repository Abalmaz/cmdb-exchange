import pytest


@pytest.fixture()
def nested_data():
    return [{
        'master_id': 123,
        'environments': [
            {'id': 111, 'name': 'Web Server', 'status': 'Run',
             'risk_profile_data': {'GxP': True}},
            {'id': 112, 'name': 'Web Server', 'status': 'New',
             'risk_profile_data': {'GxP': True}},
            {'id': 113, 'name': 'Web Server', 'status': 'Run',
             'risk_profile_data': {'GxP': False}}
        ]
    },
        {
            'master_id': 456,
            'environments': [
                {'id': 211, 'name': 'Mobile app', 'status': 'Build',
                 'risk_profile_data': {'GxP': True}},
                {'id': 212, 'name': 'Mobile app', 'status': 'Run',
                 'risk_profile_data': {'GxP': True}},
                {'id': 213, 'name': 'Mobile app', 'status': 'Run',
                 'risk_profile_data': {'GxP': True}}
            ]
        }
    ]