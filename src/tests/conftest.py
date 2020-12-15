import pytest


@pytest.fixture()
def python_nested_data():
    return [
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
         'security': None,
         'users': [
             {
                 'user_name': 'JAULIKAR, DILAWAR M',
                 'phone': '908-901-1673',
                 'email': 'DILAWAR.M.JAULIKAR@PFIZER.COM',
                 'id': 'SC213359',
                 'status': 'Active',
                 'comments': '',
                 'type': 'APPLICATION SUPPORT OWNER'
             },
             {
                 'user_name': 'JENSEN, KENT',
                 'phone': 'UNKNOWN',
                 'email': 'KENT.JENSEN@PFIZER.COM',
                 'id': 'SC2038363',
                 'status': 'Active',
                 'comments': '',
                 'type': 'APPLICATION SUPPORT - PRIMARY'
             },
{
                 'user_name': 'JENSEN, KENT',
                 'phone': 'UNKNOWN',
                 'email': 'KENT.JENSEN@PFIZER.COM',
                 'id': 'SC2038363',
                 'status': 'Active',
                 'comments': '',
                 'type': 'APPLICATION SUPPORT LEAD'
             }
         ],
         'risk_profile': None
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
         'security': None,
         'users': [
             {
                 'user_name': 'DL-BT-DIGITALMARKETING, DL',
                 'phone': '+1 212 7333334',
                 'email': 'DL-BT-DIGITALMARKETING@PFIZER.COM',
                 'id': 'SC2000222',
                 'status': 'Active',
                 'comments': '',
                 'type': 'APPLICATION SUPPORT - PRIMARY'
             },
             {
                 'user_name': 'JAULIKAR, DILAWAR M',
                 'phone': '908-901-1673',
                 'email': 'DILAWAR.M.JAULIKAR@PFIZER.COM',
                 'id': 'SC213359',
                 'status': 'Active',
                 'comments': '',
                 'type': 'APPLICATION SUPPORT OWNER'
             }
         ],
         'risk_profile': {
             'iprm_id': 3275727,
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
            'type': 'BUSINESS APPLICATION OWNER'
        },
        {
            'user_name': 'JAULIKAR, DILAWAR M',
            'phone': '908-901-1673',
            'email': 'DILAWAR.M.JAULIKAR@PFIZER.COM',
            'id': 'SC213359',
            'status': 'Active',
            'comments': '',
            'type': 'APPLICATION SUPPORT OWNER'
        },
        {
            'user_name': 'HOLDA, PAUL',
            'phone': '+1 (973) 6605928',
            'email': 'PAUL.X.HOLDA@GSK.COM',
            'id': 'SC1302458',
            'status': 'Inactive',
            'comments': '',
            'type': 'BT APPLICATION STEWARD'
        }
    ]
}
]


@pytest.fixture(scope="session")
def environment_users_csv_file(tmpdir_factory):
    csv_file = tmpdir_factory.mktemp('mydir').join('AppSearchContactExport_test_Environment.csv')
    csv_data = '''CIID,Application Name,Contact  Name,CI Contact Type,Contact Phone,Email,SC Contact ID,Contact Status,Comments
SC2634359,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 4.0 - AMER - STAGING - DRUPAL-US,"JAULIKAR, DILAWAR M",APPLICATION SUPPORT OWNER,908-901-1673,DILAWAR.M.JAULIKAR@PFIZER.COM,SC213359,Active,
SC2634359,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 4.0 - AMER - STAGING - DRUPAL-US,"JENSEN, KENT",APPLICATION SUPPORT - PRIMARY,UNKNOWN,KENT.JENSEN@PFIZER.COM,SC2038363,Active,
SC2634359,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 4.0 - AMER - STAGING - DRUPAL-US,"JENSEN, KENT",APPLICATION SUPPORT LEAD,UNKNOWN,KENT.JENSEN@PFIZER.COM,SC2038363,Active,
SC2865392,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 1.0 - APAC - PRODUCTION - DRUPAL-PH,"DL-BT-DIGITALMARKETING, DL",APPLICATION SUPPORT - PRIMARY,+1 212 7333334,DL-BT-DIGITALMARKETING@PFIZER.COM,SC2000222,Active,
SC2865392,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 1.0 - APAC - PRODUCTION - DRUPAL-PH,"JAULIKAR, DILAWAR M",APPLICATION SUPPORT OWNER,908-901-1673,DILAWAR.M.JAULIKAR@PFIZER.COM,SC213359,Active,
'''
    csv_file.write(csv_data)
    return csv_file


@pytest.fixture(scope="session")
def master_users_csv_file(tmpdir_factory):
    csv_file = tmpdir_factory.mktemp('mydir').join('AppSearchContactExport_test_Master.csv')
    csv_data = '''CIID,Application Name,Contact  Name,CI Contact Type,Contact Phone,Email,SC Contact ID,Contact Status,Comments
SC2265892,PRODUCT WEBSITE: ADVIL.COM,"FOX, BRETT S",BUSINESS APPLICATION OWNER,+1.484.865.3628,BRETT.FOX@PFIZER.COM,SC1277180,Active,
SC2265892,PRODUCT WEBSITE: ADVIL.COM,"JAULIKAR, DILAWAR M",APPLICATION SUPPORT OWNER,908-901-1673,DILAWAR.M.JAULIKAR@PFIZER.COM,SC213359,Active,
SC2265892,PRODUCT WEBSITE: ADVIL.COM,"HOLDA, PAUL",BT APPLICATION STEWARD,+1 (973) 6605928,PAUL.X.HOLDA@GSK.COM,SC1302458,Inactive,
'''
    csv_file.write(csv_data)
    return csv_file


@pytest.fixture(scope="session")
def cmdb_data_csv_file(tmpdir_factory):
    csv_file = tmpdir_factory.mktemp('mydir').join('cmdb-sample-download.csv')
    csv_data = '''CIID,Master CI ID,Application Name,Deployment Name,Deployment Description,Status,Env. Type,Application Deployment Type,Location,Org Level 1,Org Level 2,Org Level 3,Business Critical,IPRM Questionnaire ID,CRP Type,Compliance Rating Status,SDLC Path,DR/RTO Tier,SOX Value,GxP?,GCP?,GDP?,GLP?,GMP?,GPvP?,EEA PI/SPI,MA 201,Sales,ACA,SMD,Data Classification,Cybersecurity Protection Level,Access?,Detect?,Identify?,Prevent?,Response?,Regional,Global,I&AM Authentication,Used in Lab?,CI Mgmt Group,Under Change Mgmt?,SLA Support ID,Primary URL,Key Use Periods,Application Externally Accessible,Externally Hosted Application,Country Solution Hosted In,Hosting Vendor,Daily Monitoring of Site,Cookies Stored?,Customer Info Stored?
SC2634359,SC2265892,PRODUCT WEBSITE: ADVIL.COM,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 4.0 - AMER - STAGING - DRUPAL-US,Internet Website,Run,Staging,Web Site,AMER,CONSUMER,DSE,DAIA - Digital Services,False,,,,,,,,,,,,,,,,,,,,,,,,,,,,False,GBL-BT-DIGITAL MARKETING,False,,acrfb.advil.com,,True,False,,ACQUIA,,False,False
SC2865392,SC2265892,PRODUCT WEBSITE: ADVIL.COM,PRODUCT WEBSITE: ADVIL.COM (CONSUMER) - 1.0 - APAC - PRODUCTION - DRUPAL-PH,Internet Website,Run,Production,Web Site,APAC,CONSUMER,DSE,DAIA - Digital Services,False,3275727,Direct to Business,Confirmed,Baseline,Tier 4,False,False,False,False,False,False,False,False,False,False,False,False,,,,,,,,False,False,Unknown,False,GBL-BT-DIGITAL MARKETING,False,,advil.com.ph,,True,True,PHILIPPINES,ACQUIA,,False,False
'''
    csv_file.write(csv_data)
    return csv_file
