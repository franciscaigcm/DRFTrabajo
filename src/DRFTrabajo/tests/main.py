# main.py
import sys
sys.path.append('src')  # Ensure the src directory is in the Python path

from DRFTrabajo.funcs.uf import get_ufs
from datetime import date

def main():
    last_uf_known_date = date(2023, 12, 9)  # Must be day 9
    last_uf_value =  36607.69
    new_ipc = 0.7  # IPC variation as a percentage

    # Call the get_ufs function and print its return value
    ufs = get_ufs(last_uf_known_date, last_uf_value, new_ipc)
    for date_key, uf_value in ufs.items():
        print(f"{date_key}: {uf_value}")

if __name__ == "__main__":
    main()


from DRFTrabajo.FixedIncome import CLBond, FixedCoupon

# Crear instancias y utilizar los métodos
from datetime import date, timedelta

# Example usage in main.py
payment_date = date.today() + timedelta(days=30)  # This is just an example, adjust accordingly
coupon = FixedCoupon(amortization=10, interest=5, residual=90, payment_date=payment_date)
bond = CLBond(coupons=[coupon])

# Ejemplo de uso de los métodos
notional = 1000000  # Ejemplo de valor nominal
rate = 0.05  # Ejemplo de tasa de interés
today = date.today()  # Fecha de hoy

# If TERA wasn't provided during initialization, calculate it
if bond.tera is None:
    bond.set_tera()

value = bond.get_value(notional, rate, today)
tera = bond.set_tera()
dv01 = bond.get_dv01(notional)

print(f"Valor del bono: {value}")
print(f"TERA del bono: {tera}")
print(f"DV01 del bono: {dv01}")
