from marshmallow import Schema, fields

from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.default import CmdbItemBuilder


class RiskProfileSchema(Schema):
    iprm_id = fields.Str()
    sdlc_path = fields.Str()
    soc_value = fields.Bool()
    gxp = fields.Bool()


class EnvironmentSchema(Schema):
    ciid = fields.String()
    deployment_name = fields.Str()
    description = fields.Str()
    status = fields.Str()
    env_type = fields.Str()
    url = fields.Str()
    risk_profile = fields.Nested(RiskProfileSchema)


class MasterSchema(Schema):
    master_ciid = fields.Str()
    application = fields.Str()
    environments = fields.Nested(EnvironmentSchema)

"""
    Example import data from 'csv' file using library
"""


importer = CmdbExchange.create_importer(format='csv',
                                        build_schema=CmdbItemBuilder(MasterSchema()))
with importer.open('/home/user/Downloads/test_upload.csv') as opened_file:
    data = importer.push(opened_file)


"""
    Example export recursively-nested python data to 'csv' file 
"""

exporter = CmdbExchange.create_exporter('csv', MasterSchema())
exporter.export('/home/user/Downloads/test_download.csv', data)
