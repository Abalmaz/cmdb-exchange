import csv
from csv import DictWriter


class CSVFormat:
    title = 'csv'
    extensions = ('csv',)

    @classmethod
    def get_column_name(cls, filename):
        with open(filename) as f:
            d_reader = csv.DictReader(f)
            headers = d_reader.fieldnames
        return headers

    @classmethod
    def get_data(cls, steam):
        csvreader = csv.reader(steam)
        parsed_csv = list(csvreader)
        data_rows = parsed_csv[1:]  # discard column names
        return data_rows

    @classmethod
    def export_set(cls, filename, data, fieldnames, **kwargs):
        writer_cls = DictWriter
        with open(filename, 'w') as f:
            writer = writer_cls(f, fieldnames)
            writer.writerows(data)
