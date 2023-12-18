# main.py
import sys
from datetime import date, timedelta

sys.path.append('src')

from DRFTrabajo.funcs.uf import get_ufs
from DRFTrabajo.FixedIncome import CLBond, FixedCoupon

def main():
    last_uf_known_date = date(2023, 12, 9)  # Debe ser el día 9
    last_uf_value = 36607.69
    new_ipc = 0.7  # Variación del IPC como porcentaje

    # Llama a la función get_ufs e imprime su valor de retorno
    ufs = get_ufs(last_uf_known_date, last_uf_value, new_ipc)
    for date_key, uf_value in ufs.items():
        print(f"{date_key}: {uf_value}")

    # Definiciones para FixedCoupon y CLBond
    start_date = date.today()  # o la fecha real de inicio del cupón
    residual = 100  # valor residual
    interest = 5  # interés
    amortization = 10  # amortización

    # Crear instancias y utilizar los métodos
    payment_date = date.today() + timedelta(days=30)  
    coupon = FixedCoupon(payment_date=payment_date, start_date=start_date, residual=residual, interest=interest, amortization=amortization)
    
    bond = CLBond(coupons=[coupon])

    if bond.tera is None:
        bond.set_tera()

    notional = 1000000  # Valor nominal
    today = date.today()

    value = bond.get_value(notional, bond.tera, today)
    tera = bond.tera

    # Calcula la duración del bono
    duration = bond.get_duration(bond.tera, today)
    
    # Calcula el DV01 del bono usando la duración
    dv01 = bond.get_dv01(notional, bond.tera, today)

    print(f"Valor del bono: {value}")
    print(f"TERA del bono: {tera}")
    print(f"DV01 del bono: {dv01}")
    print(f"Duración del bono: {duration}")

if __name__ == "__main__":
    main()
