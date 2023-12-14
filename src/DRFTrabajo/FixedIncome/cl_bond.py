import numpy as np
from scipy.optimize import newton
from datetime import date
from .fixed_coupon import FixedCoupon

class CLBond:
    def __init__(self, coupons):
        self.coupons = coupons
        self.tera = None

    def set_tera(self):
        # Define una función objetivo para calcular la TERA
        def objective(tera):
            return sum(coupon.residual / (1 + tera/100) ** (coupon.days / 365) for coupon in self.coupons) - 100
        
        # Usa el método de Newton para encontrar la TERA que hace que la función objetivo sea 0
        self.tera = newton(objective, x0=0)

    def get_value(self, notional: float, rate: float, current_date: date) -> float:
        # Asume que la tasa es la TIR y calcula el valor presente de los flujos futuros
        vp = sum(coupon.residual / (1 + rate/100) ** ((current_date - coupon.payment_date).days / 365) for coupon in self.coupons)
        value_par = round(100 * (1 + self.tera/100) ** (current_date - self.coupons[0].payment_date).days / 365, 8)
        precio = round(100 * vp / value_par, 4)
        amount_to_pay = notional * precio / 100  # Notional es el número de unidades
        return amount_to_pay

    def get_dv01(self, notional: float) -> float:
        original_value = self.get_value(notional, self.tera, date.today())
        new_value = self.get_value(notional, self.tera + 0.01, date.today())
        return (new_value - original_value) * 10000  # Convertir de porcentaje a puntos básicos
