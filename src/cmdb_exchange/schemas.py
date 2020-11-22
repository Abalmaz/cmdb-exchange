from marshmallow import Schema, fields, validate,  pre_load, \
    validates_schema, ValidationError


class PersonTypeSchema(Schema):
    type = fields.Str()


class PersonSchema(Schema):
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Email()
    id = fields.Str()
    status = fields.Str()
    comments = fields.Str()
    type = fields.Nested(PersonTypeSchema)


class SecuritySchema(Schema):
    cybersecurity_protection_level = fields.Str(skip_if=None)
    access = fields.Bool(skip_if='')
    detect = fields.Bool(skip_if='')
    identify = fields.Bool(skip_if='')
    prevent = fields.Bool(skip_if='')
    response = fields.Bool(skip_if='')


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
    regional = fields.Bool()
    globals = fields.Bool()
    is_auth = fields.Str()

    @pre_load
    def set_sdlc_path(self, data, **kwargs):
        if data['sdlc_path'] == '':
            data['sdlc_path'] = 'Baseline'
        return data

    @pre_load
    def set_iprm_id(self, data, **kwargs):
        data['iprm_id'] = data['iprm_id'][0:7]
        return data

    @validates_schema
    def validate_sox_value(self, data, **kwargs):
        if data["sdlc_path"] == "Validation" and data["sox_value"] is False:
            raise ValidationError("If 'SDLC path' is 'Validation' 'Sox value' must be True")


class EnvironmentSchema(Schema):
    ciid = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(["New", "Build", "Run", "Decommisioned"]))
    env_type = fields.Str()
    app_deployment_type = fields.Str()
    location = fields.Str()
    business_critical = fields.Bool()
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
    risk_profile = fields.Nested(RiskProfileSchema)
    security = fields.Nested(SecuritySchema)
    users = fields.Nested(PersonSchema, many=True)

    @pre_load
    def set_business_critical(self, data, **kwargs):
        if data['business_critical'] == '':
            data['business_critical'] = True
        return data


class MasterSchema(Schema):
    master_ciid = fields.Str()
    application = fields.Str()
    org_level_1 = fields.Str()
    org_level_2 = fields.Str()
    org_level_3 = fields.Str()
    environments = fields.Nested(EnvironmentSchema, many=True)
    users = fields.Nested(PersonSchema, many=True)
