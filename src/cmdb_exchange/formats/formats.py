import csv
from csv import DictWriter


class Format:

    def get_column_name(self, data):
        raise NotImplementedError

    def get_data(self, data):
        raise NotImplementedError

    @classmethod
    def export_s0et0(cls, *args, **kwargs):
        raise NotImplementedError


class CSVFormat(Format):

    @classmethod
    def get_column_name(cls, steam):
        csvreader = csv.reader(steam)
        headers = next(csvreader)
        return headers

    @classmethod
    def get_data(cls, steam):
        csvreader = csv.reader(steam)
        data_rows = list(csvreader)
        return data_rows

    @classmethod
    def export_set(cls, filename, data, fieldnames, **kwargs):
        writer_cls = DictWriter
        with open(filename, 'w') as f:
            writer = writer_cls(f, fieldnames)
            writer.writeheader()
            writer.writerows(data)
