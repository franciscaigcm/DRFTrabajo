from datetime import date, timedelta
from calendar import monthrange

def get_ufs(last_uf_known_date: date, last_uf_value: float, new_ipc: float) -> dict[date, float]:
    ufs = {}  # Este diccionario almacenará los resultados
    days_in_month = monthrange(last_uf_known_date.year, last_uf_known_date.month)[1]
    
    for day in range(days_in_month):
        new_date = last_uf_known_date + timedelta(days=day)
        uf_value = round(last_uf_value * (1 + new_ipc) ** (day / days_in_month), 2)
        ufs[new_date] = uf_value

    return ufs

# Ejemplo de uso
last_uf_date = date(2023, 1, 1)
last_uf_value = 30000
new_ipc = 0.002  # 0.2%

ufs_calculated = get_ufs(last_uf_date, last_uf_value, new_ipc)