from csv import DictReader, DictWriter


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


class CSVFormatWriter(DictWriter):
    schema = None

    def __init__(self, f, fieldnames=None, *args, **kwargs):
        if fieldnames is None and self.schema is not None:
            fieldnames = list(self.schema._declared_fields)
        DictWriter.__init__(self, f, fieldnames, *args, **kwargs)

    def writerow(self, rowdict):
        if self.schema:
            data = self.schema.dump(rowdict)
            rowdict = data
        return DictWriter.writerow(self, rowdict)

    def writeheader(self):
        header = dict(zip(self.fieldnames, self.fieldnames))
        DictWriter.writerow(self, header)

    @classmethod
    def export_from_schema(cls, schema):
        return type(
            "CSVFormatWriter",
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
    def export_set(cls, data, filename, schema=None, fields=None,  **kwargs):
        writer_cls = CSVFormatWriter
        if schema:
            writer_cls = CSVFormatWriter.export_from_schema(schema)
        with open(filename, 'w') as f:
            fieldnames = fields
            writer = writer_cls(f, fieldnames=fieldnames, **kwargs)
            writer.writeheader()
            for line in data:
                writer.writerow(line)

