from .fixed_coupon import FixedCoupon
from datetime import date

class CLBond:
    def __init__(self, coupons, tera=None):
        self.coupons = coupons  # List of FixedCoupon instances
        self.tera = tera  # Optional, to be calculated if not provided

    def set_tera(self):
        # Logic to calculate and set the TER
        pass

    def get_value(self, notional: float, rate: float, date: date) -> float:
        # Logic to calculate the bond value
        pass

    def get_dv01(self, notional: float) -> float:
        # Logic to calculate the DV01
        pass
