import csv
from csv import DictWriter


class Format:

    def get_column_name(self, data):
        raise NotImplementedError


    @classmethod
    def import_set(cls, data):
        raise NotImplementedError

    @classmethod
    def export_set(cls, *args, **kwargs):
        raise NotImplementedError


class CSVFormat(Format):

    title = 'csv'
    extensions = ('csv',)

    @classmethod
    def get_column_name(cls, steam):
        csvreader = csv.DictReader(steam)
        headers = csvreader.fieldnames
        return headers

    @classmethod
    def import_set(cls, steam):
        csvreader = csv.DictReader(steam)
        data_rows = list(csvreader)
        return data_rows


    #TODO rename
    @classmethod
    def export_set(cls, filename, data, fieldnames, headers, **kwargs):
        writer_cls = DictWriter
        with open(filename, 'w') as f:
            writer = writer_cls(f, fieldnames)
            writer.writerow(headers)
            writer.writerows(data)
