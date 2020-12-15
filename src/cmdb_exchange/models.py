import dataclasses
from dataclasses import dataclass, field
from typing import List


@dataclass
class Base:
    @classmethod
    def get_keys(cls):
        return [field.name for field in dataclasses.fields(cls)]


@dataclass
class PersonType(Base):
    type: str


@dataclass
class Person(Base):
    id: str
    user_name: str
    email: str
    status: str
    type: PersonType
    phone: str = None
    comments: str = None


@dataclass
class Security(Base):
    cybersecurity_protection_level: str
    access: bool
    detect: bool
    identify: bool
    prevent: bool
    response: bool


@dataclass
class RiskProfile(Base):
    iprm_id: int
    cpr_type: str
    compliance_rating_status: str
    sdlc_path: str
    dr_rto_tier: str
    sox_value: bool
    gxp: bool
    gcp: bool
    gdp: bool
    glp: bool
    gmp: bool
    gpvp: bool
    eea_pi_spi: bool
    ma201: bool
    sales: bool
    aca: bool
    smd: bool
    data_class: bool
    regional: bool
    globals: bool
    is_auth: str


@dataclass
class Environment(Base):
    ciid: str
    name: str
    description: str
    status: str
    env_type: str
    app_deployment_type: str
    location: str
    business_critical: str
    used_in_lab: bool
    ci_mgmt_group: str
    under_change_mgmt: bool
    primary_url: str
    key_used_periods: str
    app_externally_accessible: str
    country_solution_hosted_in: str
    hosting_vendor: str
    sla_support_id: str
    externally_hosted_app: bool
    country_solution_hosted_in: str
    daily_monitoring_site: str
    cookies_stored: bool
    customer_into_stored: bool
    risk_profile: RiskProfile
    security: Security
    users: List[Person] = field(default_factory=list)


@dataclass
class CmdbItem(Base):
    master_ciid: str
    application: str
    org_level_1: str
    org_level_2: str
    org_level_3: str
    environments: List[Environment] = field(default_factory=list)
    users: List[Person] = field(default_factory=list)
