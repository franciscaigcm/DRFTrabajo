from datetime import date

class FixedCoupon:
    def __init__(self, payment_date, start_date, amortization, interest, residual):
        if not all(isinstance(d, date) for d in [payment_date, start_date]):
            raise ValueError("Las fechas deben ser instancias de datetime.date")
        if not all(isinstance(n, (int, float)) and n >= 0 for n in [amortization, interest, residual]):
            raise ValueError("Amortización, interés y residual deben ser números no negativos")

        self.payment_date = payment_date
        self.start_date = start_date
        self.amortization = amortization
        self.interest = interest
        self.residual = residual

    def cash_flow(self):
        return self.amortization + self.interest

    def __str__(self):
        return f"Cupón: Pago={self.payment_date}, Inicio={self.start_date}, Amortización={self.amortization}, Interés={self.interest}, Residual={self.residual}"



