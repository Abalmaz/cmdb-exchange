from csv import DictReader, DictWriter


from src.pfizer_library.utils import flatten_data


class CSVFormatReader(DictReader):
    schema = None

    def __next__(self):
        obj = DictReader.__next__(self)
        if self.schema:
            data = self.schema.load(obj)
            obj = data
        return obj

    def next(self):
        if not hasattr(DictReader, "__next__"):
            DictReader.__next__ = DictReader.next
        return self.__next__()

    @classmethod
    def import_from_schema(cls, schema):
        return type(
            'CSVFormatReader',
            (cls, object),
            {"schema": schema}
        )


class CSVFormat:
    title = 'csv'
    extensions = ('csv',)

    @classmethod
    def import_set(cls, filename, schema=None, **kwargs):
        dset = []
        with open(filename) as f:
            if schema:
                reader = CSVFormatReader.import_from_schema(schema)
                rows = reader(f, **kwargs)
            else:
                rows = CSVFormatReader(f, **kwargs)
            for row in rows:
                dset.append(row)
        return dset

    @classmethod
    def export_set(cls, data, filename, many=True,
                   schema=None, fieldnames=None, **kwargs):
        writer_cls = DictWriter
        if schema:
            serialized_data = schema.dump(data, many=many)
            data = serialized_data
        with open(filename, 'w') as f:
            flatt_data = flatten_data(data)
            if fieldnames is None:
                fieldnames = flatt_data[0].keys()
            writer = writer_cls(f, fieldnames)
            writer.writerows(flatt_data)
