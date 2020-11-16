from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.export import EnvironmentsUserFile, MasterUsersFile, CmdbDataFile

"""
This is example, how export to 'csv' format files from python data.
For demonstrate we have data with one Master, which has two Environments
"""


example_cmdb_data = [
{
    'master_ciid': 'SC2265892',
    'application': 'PRODUCT WEBSITE: ADVIL.COM',
    'org_level_1': 'CONSUMER',
    'org_level_2': 'DSE',
    'org_level_3': 'DAIA - Digital Services',
    'environments': [
        {'ciid': 'SC2634359',
         'name': "PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 4.0 - AMER - STAGING - DRUPAL-US",
         'description': 'Internet Website',
         'status': 'Run',
         'env_type': 'Staging',
         'app_deployment_type': 'Web Site',
         'location': 'AMER',
         'business_critical': False,
         'used_in_lab': False,
         'ci_mgmt_group': 'GBL-BT-DIGITAL MARKETING',
         'under_change_mgmt': False,
         'sla_support_id': '',
         'primary_url': 'acrfb.advil.com',
         'key_used_periods': '',
         'app_externally_accessible': True,
         'externally_hosted_app': False,
         'country_solution_hosted_in': '',
         'hosting_vendor': 'ACQUIA',
         'daily_monitoring_site': '',
         'cookies_stored': False,
         'customer_into_stored': False,
         'security': {
             'cybersecurity_protection_level': '',
             'access': '',
             'detect': '',
             'identify': '',
             'prevent': '',
             'response': ''

         },
         'users': [
             {
                 'user_name': 'JAULIKAR, DILAWAR M',
                 'phone': '908-901-1673',
                 'email': 'DILAWAR.M.JAULIKAR@PFIZER.COM',
                 'id': 'SC213359',
                 'status': 'Active',
                 'comments': '',
                 'type': {'type': 'APPLICATION SUPPORT OWNER'}
             },
             {
                 'user_name': 'JENSEN, KENT',
                 'phone': 'UNKNOWN',
                 'email': 'KENT.JENSEN@PFIZER.COM',
                 'id': 'SC2038363',
                 'status': 'Active',
                 'comments': '',
                 'type': {'type': 'APPLICATION SUPPORT - PRIMARY'}
             },
{
                 'user_name': 'JENSEN, KENT',
                 'phone': 'UNKNOWN',
                 'email': 'KENT.JENSEN@PFIZER.COM',
                 'id': 'SC2038363',
                 'status': 'Active',
                 'comments': '',
                 'type': {'type': 'APPLICATION SUPPORT LEAD'}
             }
         ],
         'risk_profile': {
             'iprm_id': '',
             'cpr_type': '',
             'compliance_rating_status': '',
             'sdlc_path': '',
             'dr_rto_tier': '',
             'sox_value': '',
             'gxp': '',
             'gcp': '',
             'gdp': '',
             'glp': '',
             'gmp': '',
             'gpvp': '',
             'eea_pi_spi': '',
             'ma201': '',
             'sales': '',
             'aca': '',
             'smd': '',
             'data_class': '',
             'regional': '',
             'globals': '',
             'is_auth': ''
         }
         },
    {
        'ciid': 'SC2865392',
         'name': "PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 1.0 - APAC - PRODUCTION - DRUPAL-PH",
         'description': 'Internet Website',
         'status': 'Run',
         'env_type': 'Production',
         'app_deployment_type': 'Web Site',
         'location': 'APAC',
         'business_critical': False,
         'used_in_lab': False,
         'ci_mgmt_group': 'GBL-BT-DIGITAL MARKETING',
         'under_change_mgmt': False,
         'sla_support_id': '',
         'primary_url': 'advil.com.ph',
         'key_used_periods': '',
         'app_externally_accessible': True,
         'externally_hosted_app': True,
         'country_solution_hosted_in': 'PHILIPPINES',
         'hosting_vendor': 'ACQUIA',
         'daily_monitoring_site': '',
         'cookies_stored': False,
         'customer_into_stored': False,
         'security': {
             'cybersecurity_protection_level': '',
             'access': '',
             'detect': '',
             'identify': '',
             'prevent': '',
             'response': ''

         },
         'users': [
             {
                 'user_name': 'DL-BT-DIGITALMARKETING, DL',
                 'phone': '+1 212 7333334',
                 'email': 'DL-BT-DIGITALMARKETING@PFIZER.COM',
                 'id': 'SC2000222',
                 'status': 'Active',
                 'comments': '',
                 'type': {'type': 'APPLICATION SUPPORT - PRIMARY'}
             },
             {
                 'user_name': 'JAULIKAR, DILAWAR M',
                 'phone': '908-901-1673',
                 'email': 'DILAWAR.M.JAULIKAR@PFIZER.COM',
                 'id': 'SC213359',
                 'status': 'Active',
                 'comments': '',
                 'type': {'type': 'APPLICATION SUPPORT OWNER'}
             }
         ],
         'risk_profile': {
             'iprm_id': '3275727',
             'cpr_type': 'Direct to Business',
             'compliance_rating_status': 'Confirmed',
             'sdlc_path': 'Baseline',
             'dr_rto_tier': 'Tier 4',
             'sox_value': False,
             'gxp': False,
             'gcp': False,
             'gdp': False,
             'glp': False,
             'gmp': False,
             'gpvp': False,
             'eea_pi_spi': False,
             'ma201': False,
             'sales': False,
             'aca': False,
             'smd': False,
             'data_class': '',
             'regional': False,
             'globals': False,
             'is_auth': 'Unknown'
         }
         }
     ],
    'users': [
        {
            'user_name': 'FOX, BRETT S',
            'phone': '+1.484.865.3628',
            'email': 'BRETT.FOX@PFIZER.COM',
            'id': 'SC1277180',
            'status': 'Active',
            'comments': '',
            'type': {'type': 'BUSINESS APPLICATION OWNER'}
        },
        {
            'user_name': 'JAULIKAR, DILAWAR M',
            'phone': '908-901-1673',
            'email': 'DILAWAR.M.JAULIKAR@PFIZER.COM',
            'id': 'SC213359',
            'status': 'Active',
            'comments': '',
            'type': {'type': 'APPLICATION SUPPORT OWNER'}
        },
        {
            'user_name': 'HOLDA, PAUL',
            'phone': '+1 (973) 6605928',
            'email': 'PAUL.X.HOLDA@GSK.COM',
            'id': 'SC1302458',
            'status': 'Inactive',
            'comments': '',
            'type': {'type': 'BT APPLICATION STEWARD'}
        }
    ]
}
]

"""
    For creating 'csv' file with environment's users data we need:
        1. create instance of the export with suitable file builder(EnvironmentsUserFile)
        2. realize export method with passing folder path where we want to save file and the data
"""

env_user_exporter = CmdbExchange.create_exporter('csv', EnvironmentsUserFile())
env_user_exporter.export('/home/user/Documents/examples/', example_cmdb_data)

"""
    Creating 'csv' file with master's users data
"""

master_user_exporter = CmdbExchange.create_exporter('csv', MasterUsersFile())
master_user_exporter.export('/home/user/Documents/examples/', example_cmdb_data)


"""
    Creating 'csv' file with cmdb data
"""

cmdb_data_exporter = CmdbExchange.create_exporter('csv', CmdbDataFile())
cmdb_data_exporter.export('/home/user/Documents/examples/', example_cmdb_data)