import csv
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine, Statement


class BZWBKPlugin(Plugin):
    """BZWBK plugin
    """

    def get_parser(self, filename):
        return BZWBKParser(filename)


class BZWBKParser(CsvStatementParser):
    def __init__(self, filename):
        self.statement = Statement()
        self.filename = filename

        with open(self.filename, "r", encoding='utf8') as f:
            self.fin = f.read()

    def split_records(self):
        return csv.reader(self.fin, dialect='foo')

    def parse_record(self, line):
        print(line)
        stmt_line = StatementLine()
        for field, col in self.mappings.items():
            if col >= len(line):
                raise ValueError("Cannot find column %s in line of %s items "
                                 % (col, len(line)))
            rawvalue = line[col]
            value = self.parse_value(rawvalue, field)
            setattr(stmt_line, field, value)
        return stmt_line
