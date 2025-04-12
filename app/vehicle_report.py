from .report_base import BaseReport
from .util import get_vehicle_type_status_name, get_vehicle_model_status_name

class VehicleReport(BaseReport):
    def __init__(self, vehicles):
        super().__init__(filename="vehicle_report", title="Vehicle Report")
        self.vehicles = vehicles

    def get_headers(self):
        return ["Type", "Model", "Year", "License Plate", "Mileage", "Reg. Expiry"]

    def get_data_rows(self):
        rows = []
        for v in self.vehicles:
            type_ = get_vehicle_type_status_name(True).get(v.type, "-")
            model = get_vehicle_model_status_name(True).get(v.model, "-")
            reg_exp = str(v.registration_expiry_date).replace("-", ".")
            rows.append([type_, model, v.year, v.license_plate, v.current_mileage, reg_exp])
        return rows
