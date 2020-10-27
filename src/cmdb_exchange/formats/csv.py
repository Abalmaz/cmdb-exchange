import csv
from csv import DictWriter


class CSVFormat:
    title = 'csv'
    extensions = ('csv',)

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
            writer.writerows(data)
