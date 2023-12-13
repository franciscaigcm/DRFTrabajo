from datetime import date, timedelta
import calendar

class UFCalculator:
    def __init__(self, last_uf_known_date: date, last_uf_value: float, new_ipc: float):
        if last_uf_known_date.day != 9:
            raise ValueError("La fecha de la última UF conocida debe ser el día 9 del mes.")
        self.last_uf_known_date = last_uf_known_date
        self.last_uf_value = last_uf_value
        self.new_ipc = new_ipc / 100  # Convertir a decimal para el cálculo

    def calculate_ufs(self, end_date: date) -> dict[date, float]:
        days_in_month = calendar.monthrange(self.last_uf_known_date.year, self.last_uf_known_date.month)[1]
        uf_values = {}
        for i in range((end_date - self.last_uf_known_date).days + 1):
            current_date = self.last_uf_known_date + timedelta(days=i)
            days_since_last_uf = (current_date - self.last_uf_known_date).days
            uf_value = round(self.last_uf_value * (1 + self.new_ipc) ** (days_since_last_uf / days_in_month), 2)
            uf_values[current_date] = uf_value
        return uf_values

# La función get_ufs que será accesible desde fuera del módulo
def get_ufs(last_uf_known_date: date, last_uf_value: float, new_ipc: float) -> dict[date, float]:
    calculator = UFCalculator(last_uf_known_date, last_uf_value, new_ipc)
    end_date = date.today()  # O la fecha que necesites hasta calcular la UF
    return calculator.calculate_ufs(end_date)

# Ejemplo de uso de la función get_ufs
last_uf_known_date = date(2023, 1, 9)  # Debe ser día 9
last_uf_value = 28000.0
new_ipc = 0.5  # Suponiendo que este es el IPC porcentual como un número entero

ufs_calculated = get_ufs(last_uf_known_date, last_uf_value, new_ipc)
for date_key, uf_value in ufs_calculated.items():
    print(f"{date_key}: {uf_value}")