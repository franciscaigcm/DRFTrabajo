import numpy as np
from scipy.optimize import minimize
from datetime import date
from scipy.optimize import newton



class CLBond:
    def __init__(self, coupons, tera=None):
        self.coupons = coupons 
        self.tera = tera if tera is not None else self.set_tera()
    
    def set_tera(self, tol=1e-10, max_iter=10000):
        
        tera = self.set_tera_newton(tol=tol, max_iter=max_iter)
        if tera is not None:
            self.tera = tera
        else:
            raise ValueError("Failed to compute TERA")
    
    def set_tera_newton(self, tol=1e-10, max_iter=10000):
        def objective(tera):
            
            if tera <= -0.99:
                return float('inf')

            # Calcula el valor presente de los flujos de efectivo descontados a la TERA
            present_value = sum(coupon.cash_flow() / (1 + tera/100) ** ((coupon.payment_date - self.coupons[0].start_date).days / 365) for coupon in self.coupons)
            
            # La función debe ser igual a cero, así que restamos 100 para encontrar la TERA
            return present_value - 100

        # Usa el método de Newton-Raphson para encontrar la raíz de la función objetivo
        tera_guess = newton(func=objective, x0=0.5, tol=tol, maxiter=max_iter)
        return tera_guess    
    
    def get_value(self, notional: float, rate: float, valuation_date: date) -> float:
        if self.tera is None:
            print("Error: TERA no calculada. No se puede calcular el valor.")
            return None

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