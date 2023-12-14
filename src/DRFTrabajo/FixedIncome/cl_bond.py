import numpy as np
from scipy.optimize import newton, minimize
from datetime import date, timedelta
from .fixed_coupon import FixedCoupon

class CLBond:
    def __init__(self, coupons, tera=None):
        self.coupons = coupons  # Lista de instancias FixedCoupon
        if tera is None:
            self.set_tera()  # Si tera no se proporciona, calcula la tera automáticamente
        else:
            self.tera = tera  # Si se proporciona tera, úsala directamente

    def set_tera(self, tol=1e-6, max_iter=1000):
        tera_guess = 0.0

        for _ in range(max_iter):
            previous_tera = tera_guess
            tera_guess = self.adjust_tera(tera_guess)

            if abs(tera_guess - previous_tera) < tol:
                self.tera = tera_guess
                return

        raise RuntimeError("Failed to converge within the specified number of iterations.")

    def adjust_tera(self, current_tera):
        def objective(tera):
            return sum(coupon.residual / (1 + tera/100) ** ((coupon.payment_date - self.coupons[0].payment_date).days / 365) for coupon in self.coupons) - 100

        result = minimize(objective, x0=current_tera, tol=1e-10)
        if result.success:
            return result.x[0]
        else:
            raise RuntimeError(f"Failed to converge. Message: {result.message}")

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