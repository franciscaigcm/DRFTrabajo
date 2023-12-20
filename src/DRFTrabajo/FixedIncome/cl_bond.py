import numpy as np
from scipy.optimize import minimize
from datetime import date

class CLBond:
    def __init__(self, coupons, tera=None):
        self.coupons = coupons  # Lista de instancias FixedCoupon
        self.tera = tera if tera is not None else self.set_tera()

    def set_tera(self, tol=1e-6, max_iter=1000):
        tera_guess = 0.5

        for _ in range(max_iter):
            previous_tera = tera_guess
            tera_guess = self.adjust_tera(tera_guess)

            if abs(tera_guess - previous_tera) < tol:
                self.tera = tera_guess
                return
        raise RuntimeError("Failed to converge within the specified number of iterations.")

    def adjust_tera(self, current_tera):
        def objective(tera):
            issue_date = self.coupons[0].start_date
            total_cash_flow = sum((coupon.amortization + coupon.interest) / (1 + tera/100) ** ((coupon.payment_date - issue_date).days / 365) for coupon in self.coupons)
            return total_cash_flow - 100

        result = minimize(objective, x0=current_tera, tol=1e-10)
        if result.success:
            return result.x[0]
        else:
            raise RuntimeError(f"Failed to converge. Message: {result.message}")
    
    def get_value(self, notional: float, rate: float, valuation_date: date) -> float:
        if self.tera is None:
            self.set_tera()

        # Calcula el total de flujos de efectivo descontando el flujo total (amortización + interés)
        total_cash_flow = sum((coupon.amortization + coupon.interest) / (1 + rate/100) ** ((coupon.payment_date - valuation_date).days / 365) for coupon in self.coupons)

        # Usar el residual del cupón vigente para calcular el valor par
        current_coupon = self.coupons[0]  # Suponiendo que es el cupón vigente
        value_par = round(current_coupon.residual * (1 + self.tera/100) ** ((valuation_date - current_coupon.start_date).days / 365), 8)

        # Calcular el precio y el monto a pagar
        precio = round(100 * total_cash_flow / value_par, 4)
        amount_to_pay = notional * precio / 100

        return amount_to_pay
    
    def get_duration(self, rate: float, valuation_date: date) -> float:
        pv = sum((coupon.amortization + coupon.interest) / (1 + rate/100) ** ((coupon.payment_date - valuation_date).days / 365) for coupon in self.coupons)
        weighted_times = [(coupon.payment_date - valuation_date).days / 365 * (coupon.amortization + coupon.interest) / (1 + rate/100) ** ((coupon.payment_date - valuation_date).days / 365) for coupon in self.coupons]
        
        duration = sum(weighted_times) / pv
        return duration

    def get_dv01(self, notional: float, rate: float, valuation_date: date) -> float:
        vp = self.get_value(notional, rate, valuation_date)
        duration = self.get_duration(rate, valuation_date)
        dv01 = vp * duration / 10000
        return dv01