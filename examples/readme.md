There are examples how work with library:

Example marshmallow schemas: 
```
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
```
example upload csv file:
```
master_ciid,application,ciid,deployment_name,description,status,env_type,url,iprm_id,sdlc_path,soc_value,gxp
SC2265886,PRODUCT WEBSITE: CALTRATE,SC2550040,PRODUCT WEBSITE: CALTRATE (CONSUMER)',"CALTRATE.COM IS TRANSITIIOND TO DRUPAL PLATFORM, HOSTED EXTERNALLY BY VERIZON",Run,Staging,http://stg.caltrate.pfizer.com,3275727,Baseline,True,True
SC2265886,PRODUCT WEBSITE: CALTRATE,SC2630860,PRODUCT WEBSITE: WEBINARS (DIGITAL),New website for Webinars,New,Development,webinar,3275727,Baseline,True,True
SC2465284,EXTERNAL WEBSITE: QUITWITHHELP,SC2747583,EXTERNAL WEBSITE: QUITWITHHELP (BIOPHARMA),External website,Run,Prodaction,arreterdefumeravecaide.be,3275727,Baseline,True,True
```
Result of import:
```
[{'application': 'PRODUCT WEBSITE: CALTRATE',
  'environments': {'ciid': 'SC2550040',
                   'deployment_name': "PRODUCT WEBSITE: CALTRATE (CONSUMER)'",
                   'description': 'CALTRATE.COM IS TRANSITIIOND TO DRUPAL '
                                  'PLATFORM, HOSTED EXTERNALLY BY VERIZON',
                   'env_type': 'Staging',
                   'risk_profile': {'gxp': True,
                                    'iprm_id': '3275727',
                                    'sdlc_path': 'Baseline',
                                    'soc_value': True},
                   'status': 'Run',
                   'url': 'http://stg.caltrate.pfizer.com'},
  'master_ciid': 'SC2265886'},
 {'application': 'PRODUCT WEBSITE: CALTRATE',
  'environments': {'ciid': 'SC2630860',
                   'deployment_name': 'PRODUCT WEBSITE: WEBINARS (DIGITAL)',
                   'description': 'New website for Webinars',
                   'env_type': 'Development',
                   'risk_profile': {'gxp': True,
                                    'iprm_id': '3275727',
                                    'sdlc_path': 'Baseline',
                                    'soc_value': True},
                   'status': 'New',
                   'url': 'webinar'},
  'master_ciid': 'SC2265886'},
 {'application': 'EXTERNAL WEBSITE: QUITWITHHELP',
  'environments': {'ciid': 'SC2747583',
                   'deployment_name': 'EXTERNAL WEBSITE: QUITWITHHELP '
                                      '(BIOPHARMA)',
                   'description': 'External website',
                   'env_type': 'Prodaction',
                   'risk_profile': {'gxp': True,
                                    'iprm_id': '3275727',
                                    'sdlc_path': 'Baseline',
                                    'soc_value': True},
                   'status': 'Run',
                   'url': 'arreterdefumeravecaide.be'},
  'master_ciid': 'SC2465284'}]
```
