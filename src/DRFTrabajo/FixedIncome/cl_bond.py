import numpy as np
from scipy.optimize import newton
from datetime import date
from .fixed_coupon import FixedCoupon

class CLBond:
    def __init__(self, coupons, tera=None):
        self.coupons = coupons  # List of FixedCoupon instances
        self.tera = tera if tera is not None else self.set_tera()

    def set_tera(self):
        # Define una función objetivo para calcular la TERA
        def objective(tera):
            return sum(coupon.residual / (1 + tera/100) ** ((coupon.payment_date - self.coupons[0].payment_date).days / 365) for coupon in self.coupons) - 100
        
        # Usa el método de Newton para encontrar la TERA que hace que la función objetivo sea 0
        self.tera = newton(objective, x0=0.25, tol=1e-10, maxiter=1000)
        self.tera = self.tera if self.tera is not None else 0.0
        return self.tera
    
    def get_value(self, notional: float, rate: float, valuation_date: date) -> float:
        if self.tera is None:
            self.set_tera()  # Make sure tera is calculated

        vp = sum(coupon.residual / (1 + rate/100) ** ((coupon.payment_date - valuation_date).days / 365) for coupon in self.coupons)
        first_payment_date = self.coupons[0].payment_date
        value_par = round(100 * (1 + self.tera/100) ** ((first_payment_date - valuation_date).days / 365), 8)
        precio = round(100 * vp / value_par, 4)
        amount_to_pay = notional * precio / 100  # Notional is the number of units
        return amount_to_pay

    def get_dv01(self, notional: float) -> float:
        original_value = self.get_value(notional, self.tera, date.today())
        bumped_tera = self.tera + 0.01  # Increase TERA by 0.01%
        new_value = self.get_value(notional, bumped_tera, date.today())
        dv01 = (new_value - original_value) * 10000  # Convert to basis points
        return dv01