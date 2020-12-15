# Python library for CMDB and IPRM
Python library that can translate a standardized Python data structure to a file with given extension, 
and export files to a single standardized Python data structure.

Output formats supported:
* CSV

### Installation

1. Download source code from gitlab
2. Install requirements from `requirements.txt` file

### Exporting data

1. Сreate an exporter object with an extension and the necessary builder as parameters

 > exporter = CmdbExchange.create_exporter('csv', CmdbDataBuilder())

2. Use method `export` with path to folder, where you want to create a file, 
   and data as parameters

>  exporter.export('/home/user/Documents', cmdb_data)

### Importing data

1. Сreate an importer object with an extension and the schema using for serialization data as parameters

 > importer = CmdbExchange.create_importer('csv', MasterSchema())

2. Use method `import_data` with the path to folder, where files are situated

>  data = importer.import_data('/home/user/Documents')

You can view all examples of conversions in the [examples](/examples) directory.

### Development
#### Adding new formats
1. Write a new format class inheriting from `cmdb_exchange.formats.Format` class.
2. Register new class:
```
from cmdb_exchange.formats import registry
registry.register('xxx', NewXXXFormatClass())
```
#### Run tests
>pytest
