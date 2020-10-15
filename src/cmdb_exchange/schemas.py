from marshmallow import Schema, fields


class RiskProfileSchema(Schema):
    iprm_id = fields.Int()
    cpr_type = fields.Str()
    compliance_rating_status = fields.Str()
    sdlc_path = fields.Str()
    dr_rto_tier = fields.Str()
    sox_value = fields.Bool()
    gxp = fields.Bool()
    gcp = fields.Bool()
    gdp = fields.Bool()
    glp = fields.Bool()
    gmp = fields.Bool()
    gpvp = fields.Bool()
    eea_pi_spi = fields.Bool()
    ma201 = fields.Bool()
    sales = fields.Bool()
    aca = fields.Bool()
    smd = fields.Bool()
    data_class = fields.Str()
    cybersecurity_protection_level = fields.Str()
    access = fields.Bool()
    detect = fields.Bool()
    identify = fields.Bool()
    prevent = fields.Bool()
    response = fields.Bool()
    regional = fields.Bool()
    globals = fields.Bool()
    is_auth = fields.Str()


class EnvironmentSchemas(Schema):
    ciid = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    env_type = fields.Str()
    app_deployment_type = fields.Str()
    location = fields.Str()
    org_level_1 = fields.Str()
    org_level_2 = fields.Str()
    org_level_3 = fields.Str()
    business_critical = fields.Bool()
    iprm_info = fields.Nested(RiskProfileSchema)
    used_in_lab = fields.Bool()
    ci_mgmt_group = fields.Str()
    under_change_mgmt = fields.Bool()
    sla_support_id = fields.Str()
    primary_url = fields.Url()
    key_used_periods = fields.Str()
    app_externally_accessible = fields.Bool()
    externally_hosted_app = fields.Bool()
    country_solution_hosted_in = fields.Str()
    hosting_vendor = fields.Str()
    daily_monitoring_site = fields.Str()
    cookies_stored = fields.Bool()
    customer_into_stored = fields.Bool()


class MasterSchema(Schema):
    master_ciid = fields.Str()
    application = fields.Str()
    environments = fields.Nested(EnvironmentSchemas, many=True)
