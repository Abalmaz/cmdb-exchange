from collections import OrderedDict

from src.cmdb_exchange.parser import EnvironmentsUserFileParser, FlatDataParser


class DefaultExportFile:

    @property
    def file_name(self):
        raise NotImplementedError

    @property
    def fields_name(self):
        raise NotImplementedError

    def prepare_data(self):
        raise NotImplementedError


class EnvironmentsUserFile(DefaultExportFile):
    file_name = 'ContactExportEnvironments'
    fields_name = OrderedDict((
        ('ciid', 'Env ciid'),
        ('name', 'Env name'),
        ('user_name', 'User'),
        ('role', 'User role')

    ))

    def __init__(self):
        self.data_parser = EnvironmentsUserFileParser()
        self.flat_data = FlatDataParser()

    def parse_data(self):
        return self.data_parser.result()

    def prepare_data(self):
        return self.flat_data.visit(self.parse_data())
