from collections import OrderedDict

from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.formats.csv import CSVFormat


class Registry:
    _formats = OrderedDict()

    def register(self, key, format_or_path):
        self._formats[key] = format_or_path

    def register_builtins(self):
        self.register('csv', CSVFormat())

    def get_format(self, key):
        if key not in self._formats:
            raise UnsupportedFormat(f"The '{key}' format is not available.")
        return self._formats[key]


registry = Registry()
