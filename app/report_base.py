import datetime
from flask import jsonify
from .export_utils import generate_csv, generate_xlsx, generate_pdf

class BaseReport:

    def __init__(self, filename="report", title="Report"):
        self.filename = filename
        self.title = title

    def get_headers(self):
        raise NotImplementedError("Headers must be defined")

    def get_data_rows(self):
        raise NotImplementedError("Data rows must be defined")

    def export(self, format):
        headers = self.get_headers()
        rows = self.get_data_rows()

        if format == "csv":
            return generate_csv(rows, headers, filename=f"{self.filename}.csv")
        elif format == "xlsx":
            return generate_xlsx(rows, headers, filename=f"{self.filename}.xlsx", sheet_title=self.title)
        elif format == "pdf":
            return generate_pdf(rows, headers, title=self.title, filename=f"{self.filename}.pdf")
        else:
            return jsonify("Invalid format!"), 400
