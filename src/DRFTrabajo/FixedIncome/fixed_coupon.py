class FixedCoupon:
    def __init__(self, amortization, interest, residual, days_to_payment):
        self.amortization = amortization  # The amount of principal paid
        self.interest = interest  # The interest payment
        self.residual = residual  # The remaining principal (residual value)
        self.days_to_payment = days_to_payment  # Days until the coupon payment
