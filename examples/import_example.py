from src.cmdb_exchange.cmdb import CmdbExchange
from src.cmdb_exchange.schemas import MasterSchema


'''
     For import data from files to single nested python object, you need:
      1. create a importer with extensions of files and schema as parameter
      2. call method "import_data" with path where 
         files('cmdb-sample-download.csv', 'AppSearchContactExport_Environment.csv',
         'AppSearchContactExport_20201009_Master.csv') is situated. 
'''
importer = CmdbExchange.create_importer('csv', MasterSchema())
data = importer.import_data('/home/user/Downloads/examples')
