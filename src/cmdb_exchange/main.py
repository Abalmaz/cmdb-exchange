from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.formats import registry


class CmdbExchange:

    def create_importer(self, in_stream, format=None, **kwargs):
        pass

    def create_exporter(self, format, filename,
                        schema=None, many=True, **kwargs):
        """
        Export : standardized Python data structure object to `format`.
        :param format:
        :param \\*\\*kwargs: (optional) custom configuration to the format `export_set`.
        """
        fmt = registry.get_format(format)
        if not hasattr(fmt, 'export_set'):
            raise UnsupportedFormat(f'Format {format} cannot be exported.')

        return fmt.export_set(self, filename=filename,
                              schema=schema, many=many, **kwargs)
