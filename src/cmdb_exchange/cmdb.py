from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.formats import registry


class CmdbExchange:

    @classmethod
    def create_importer(cls, format=None, **kwargs):
        fmt = registry.get_format(format)
        if not hasattr(fmt, 'import_set'):
            raise UnsupportedFormat(f'Format {format} cannot be exported.')

    @classmethod
    def create_exporter(cls, format, filename, data,
                        schema=None, many=True, **kwargs):

        fmt = registry.get_format(format)
        if not hasattr(fmt, 'export_set'):
            raise UnsupportedFormat(f'Format {format} cannot be exported.')

        return fmt.export_set(filename=filename,
                              data=data,
                              schema=schema, many=many, **kwargs)
