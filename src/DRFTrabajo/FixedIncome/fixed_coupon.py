class FixedCoupon:
    def __init__(self, amortization, interest, residual):
        self.amortization = amortization  # The amount of principal paid
        self.interest = interest  # The interest payment
        self.residual = residual  # The remaining principal (residual value)
