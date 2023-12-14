# main.py
import sys
sys.path.append('src')  # Ensure the src directory is in the Python path


from DRFTrabajo.funcs.uf import get_ufs
from datetime import date

def main():
    last_uf_known_date = date(2023, 12, 9)  # Debe ser el día 9
    last_uf_value = 36607.69
    new_ipc = 0.7  # Variación del IPC como porcentaje

    # Llama a la función get_ufs e imprime su valor de retorno
    ufs = get_ufs(last_uf_known_date, last_uf_value, new_ipc)
    for date_key, uf_value in ufs.items():
        print(f"{date_key}: {uf_value}")

if __name__ == "__main__":
    main()

from DRFTrabajo.FixedIncome import CLBond, FixedCoupon

# Crear instancias y utilizar los métodos
from datetime import date, timedelta

# Ejemplo de uso en main.py
payment_date = date.today() + timedelta(days=30)  # Este es solo un ejemplo, ajústalo según sea necesario
coupon = FixedCoupon(amortization=10, interest=5, residual=90, payment_date=payment_date)
# Se puede proporcionar la tera como argumento si se conoce
bond = CLBond(coupons=[coupon], tera=0.05)

# O permitir que se calcule automáticamente
# Si bond.tera es None, se calculará automáticamente al llamar a bond.set_tera()
if bond.tera is None:
    bond.set_tera()

notional = 1000000
rate = 0.08
today = date.today()

value = bond.get_value(notional, rate, today)
tera = bond.tera  # Ahora simplemente accede a bond.tera
dv01 = bond.get_dv01(notional)

print(f"Valor del bono: {value}")
print(f"TERA del bono: {tera}")
print(f"DV01 del bono: {dv01}")