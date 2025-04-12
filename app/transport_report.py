from .report_base import BaseReport
from .util import get_transport_cargo_name

class TransportReport(BaseReport):
    def __init__(self, transports):
        super().__init__(filename="transport_report", title="Transport Report")
        self.transports = transports

    def get_headers(self):
        return ["Date", "Origin", "Destination", "Cargo", "Amount", "Unit price", "Total price"]

    def get_data_rows(self):
        rows = []
        for t in self.transports:
            rows.append([
                t.date.strftime("%Y.%m.%d"),
                t.origin,
                t.destination,
                get_transport_cargo_name(True).get(t.cargo, "-"),
                t.amount,
                t.unit_price,
                round(t.amount * t.unit_price, 2)
            ])
        return rows
