from collections import defaultdict
from datetime import datetime, timedelta
from app.models import Transport
from .stats_base import BaseTransportStats

class LastWeekStats(BaseTransportStats):
    def __init__(self):
        self.labels = []
        self.fees = []
        self.amounts = []
        self._calculate()

    def _calculate(self):
        today = datetime.today().date()
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        day_keys = [d.strftime("%Y-%m-%d") for d in last_7_days]

        fee_map = defaultdict(float)
        amount_map = defaultdict(float)

        transports = Transport.query.filter(Transport.date >= today - timedelta(days=7)).all()
        for t in transports:
            key = t.date.strftime("%Y-%m-%d")
            fee_map[key] += t.amount * t.unit_price
            amount_map[key] += t.amount

        self.labels = [k[5:] for k in day_keys]  # pl. 04-11
        self.fees = [round(fee_map[k], 2) for k in day_keys]
        self.amounts = [round(amount_map[k], 2) for k in day_keys]

    def get_labels(self):
        return self.labels

    def get_fee_data(self):
        return self.fees

    def get_amount_data(self):
        return self.amounts
