class FixedCoupon:
    def __init__(self, payment_date, start_date, amortization, interest, residual):
        self.payment_date = payment_date
        self.start_date = start_date
        self.amortization = amortization
        self.interest = interest
        self.residual = residual


