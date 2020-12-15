from marshmallow import Schema, fields, validate,  pre_load, \
    validates_schema, ValidationError


class PersonTypeSchema(Schema):
    type = fields.Str()


class PersonSchema(Schema):
    user_name = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    id = fields.Str()
    status = fields.Str()
    comments = fields.Str()
    type = fields.Str()


class SecuritySchema(Schema):
    cybersecurity_protection_level = fields.Str()
    access = fields.Bool()
    detect = fields.Bool()
    identify = fields.Bool()
    prevent = fields.Bool()
    response = fields.Bool()


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
    gpvp = fields.Boolean()
    eea_pi_spi = fields.Boolean()
    ma201 = fields.Boolean()
    sales = fields.Boolean()
    aca = fields.Boolean()
    smd = fields.Boolean()
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
    def validate_gxp_value(self, data, **kwargs):
        if data["sdlc_path"] == "Validation" and data["gxp"] is False:
            raise ValidationError("If 'SDLC path' is 'Validation' 'GxP' must be True")

    @pre_load
    def set_gpvp(self, data, **kwargs):
        if data.get('gpvp') == '':
            data.pop('gpvp', None)
        return data

    @pre_load
    def set_ma201(self, data, **kwargs):
        if data.get('ma201') == '':
            data.pop('ma201', None)
        return data

    @pre_load
    def set_sales(self, data, **kwargs):
        if data.get('sales') == '':
            data.pop('sales', None)
        return data

    @pre_load
    def set_aca(self, data, **kwargs):
        if data.get('aca') == '':
            data.pop('aca', None)
        return data

    @pre_load
    def set_smd(self, data, **kwargs):
        if data.get('smd') == '':
            data.pop('smd', None)
        return data

    @pre_load
    def set_eea_pi_spi(self, data, **kwargs):
        if data.get('eea_pi_spi') == '':
            data.pop('eea_pi_spi', None)
        return data


class EnvironmentSchema(Schema):
    ciid = fields.Str()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(["New", "Build", "Run", "Decommissioned"]))
    env_type = fields.Str()
    app_deployment_type = fields.Str()
    location = fields.Str()
    business_critical = fields.Bool()
    used_in_lab = fields.Boolean()
    ci_mgmt_group = fields.Str()
    under_change_mgmt = fields.Boolean()
    sla_support_id = fields.Str()
    primary_url = fields.Str()
    key_used_periods = fields.Str()
    app_externally_accessible = fields.Boolean()
    externally_hosted_app = fields.Boolean()
    country_solution_hosted_in = fields.Str()
    hosting_vendor = fields.Str()
    daily_monitoring_site = fields.Str()
    cookies_stored = fields.Boolean()
    customer_into_stored = fields.Boolean()
    risk_profile = fields.Nested(RiskProfileSchema, allow_none=True)
    security = fields.Nested(SecuritySchema, allow_none=True)
    users = fields.Nested(PersonSchema, many=True, allow_none=True)

    @pre_load
    def set_business_critical(self, data, **kwargs):
        if data.get('business_critical') == '':
            data['business_critical'] = True
        return data

    @pre_load
    def set_used_in_lab(self, data, **kwargs):
        if data.get('used_in_lab') == '':
            data.pop('used_in_lab', None)
        return data

    @pre_load
    def set_cookies_stored(self, data, **kwargs):
        if data.get('cookies_stored') == '':
            data.pop('cookies_stored', None)
        return data

    @pre_load
    def set_customer_into_stored(self, data, **kwargs):
        if data.get('customer_into_stored') == '':
            data.pop('customer_into_stored', None)
        return data

    @pre_load
    def set_externally_hosted_app(self, data, **kwargs):
        if data.get('externally_hosted_app') == '':
            data.pop('externally_hosted_app', None)
        return data

    @pre_load
    def set_under_change_mgmt(self, data, **kwargs):
        if data.get('under_change_mgmt') == '':
            data.pop('under_change_mgmt', None)
        return data


class MasterSchema(Schema):
    master_ciid = fields.Str()
    application = fields.Str()
    org_level_1 = fields.Str()
    org_level_2 = fields.Str()
    org_level_3 = fields.Str()
    environments = fields.Nested(EnvironmentSchema, many=True)
    users = fields.Nested(PersonSchema, many=True, allow_none=True)
