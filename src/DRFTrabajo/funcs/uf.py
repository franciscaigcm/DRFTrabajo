from datetime import date, timedelta
from calendar import monthrange

def get_ufs(last_uf_known_date: date, last_uf_value: float, new_ipc: float) -> dict[date, float]:
    ufs = {}
    days_in_month = monthrange(last_uf_known_date.year, last_uf_known_date.month)[1]
    
    for i in range(1, days_in_month + 1):  # Empieza en 1 para incluir el día de la última UF conocida
        new_date = last_uf_known_date + timedelta(days=i-1)  # Resta 1 porque la UF ya es conocida para el día 0
        # Calcula la UF para el día actual utilizando la fórmula dada
        uf_value = round(last_uf_value * (1 + new_ipc)**(i/days_in_month), 2)
        ufs[new_date] = uf_value

    return ufs

# Ejemplo de uso
last_uf_date = date(2023, 1, 1)
last_uf_value = 30000
new_ipc = 0.02  

ufs_calculated = get_ufs(last_uf_date, last_uf_value, new_ipc)