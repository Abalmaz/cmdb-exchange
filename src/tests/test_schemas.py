import pytest
from marshmallow import EXCLUDE, ValidationError

from src.cmdb_exchange.schemas import EnvironmentSchema, RiskProfileSchema


def test_environment_schema_set_business_critical():
    schema = EnvironmentSchema()
    test_data = {'business_critical': ''}
    expected = {'business_critical': True}
    actual = schema.load(test_data, unknown=EXCLUDE)
    assert expected == actual


def test_environment_schema_status_choices_correct():
    schema = EnvironmentSchema()
    test_data = {'status': 'New', 'business_critical': True}
    data = [schema.load(test_data, unknown=EXCLUDE)]
    assert len(data) == 1


def test_environment_schema_status_choices_incorrect():
    with pytest.raises(ValidationError):
        schema = EnvironmentSchema()
        test_data = {'status': 'Stopped', 'business_critical': True}
        schema.load(test_data, unknown=EXCLUDE)


def test_risk_profile_schema_iprm_cut():
    schema = RiskProfileSchema()
    test_data = {'iprm_id': '3172210 v1.1 (Requirements)', 'sdlc_path': ''}
    expected_iprm_id = 3172210
    actual = schema.load(test_data, unknown=EXCLUDE)['iprm_id']
    assert expected_iprm_id == actual


def test_risk_profile_schema_set_sdlc_path():
    schema = RiskProfileSchema()
    test_data = {'iprm_id': '3172210 v1.1 (Requirements)', 'sdlc_path': ''}
    expected_sdlc_path = 'Baseline'
    actual = schema.load(test_data, unknown=EXCLUDE)['sdlc_path']
    assert expected_sdlc_path == actual


def test_risk_profile_schema_sox_value_correct():
    schema = RiskProfileSchema()
    test_data = {'iprm_id': '3172210 v1.1 (Requirements)', 'sdlc_path': 'Validation', 'sox_value': True}
    data = [schema.load(test_data, unknown=EXCLUDE)]
    assert len(data) == 1


def test_risk_profile_schema_sox_value_incorrect():
    with pytest.raises(ValidationError):
        schema = RiskProfileSchema()
        test_data = {'iprm_id': '3172210 v1.1 (Requirements)', 'sdlc_path': 'Validation', 'sox_value': False}
        schema.load(test_data, unknown=EXCLUDE)
