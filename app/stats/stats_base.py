class BaseTransportStats:
    def get_labels(self):
        raise NotImplementedError()

    def get_fee_data(self):
        raise NotImplementedError()

    def get_amount_data(self):
        raise NotImplementedError()

    def to_json(self):
        return {
            "labels": self.get_labels(),
            "fee_values": self.get_fee_data(),
            "amount_values": self.get_amount_data()
        }
