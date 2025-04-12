from datetime import datetime
from collections import defaultdict
from app.models import Transport
from .stats_base import BaseTransportStats

class MonthlyStats(BaseTransportStats):
    def __init__(self):
        self.transports = Transport.query.all()
        self.labels = []
        self.fees = []
        self.amounts = []
        self._calculate()

    def _calculate(self):
        monthly_fee = defaultdict(float)
        monthly_amount = defaultdict(float)

        for t in self.transports:
            if t.date:
                key = t.date.strftime("%Y-%m")
                monthly_fee[key] += t.amount * t.unit_price
                monthly_amount[key] += t.amount

        current_year = datetime.today().year
        full_year_keys = [f"{current_year}-{str(m).zfill(2)}" for m in range(1, 13)]

        contains_current_year = any(k.startswith(str(current_year)) for k in monthly_fee.keys())

        if contains_current_year:
            self.labels = full_year_keys
        else:
            self.labels = sorted(monthly_fee.keys())

        self.fees = [round(monthly_fee[k], 2) if k in monthly_fee else 0 for k in self.labels]
        self.amounts = [round(monthly_amount[k], 2) if k in monthly_amount else 0 for k in self.labels]

    def get_labels(self):
        return self.labels

    def get_fee_data(self):
        return self.fees

    def get_amount_data(self):
        return self.amounts
