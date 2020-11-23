from src.cmdb_exchange.exceptions import UnsupportedFormat
from src.cmdb_exchange.formats.formats import CSVFormat


class Registry:
    _formats = {}

    def register(self, key, fmt):
        self._formats[key] = fmt

    def register_builtins(self):
        self.register('csv', CSVFormat())

    def get_format(self, key):
        if key not in self._formats:
            raise UnsupportedFormat(f"The '{key}' format is not available.")
        return self._formats[key]


registry = Registry()
registry.register_builtins()
