# main.py
import sys
sys.path.append('src')  # Ensure the src directory is in the Python path

from DRFTrabajo.funcs.uf import get_ufs
from datetime import date

def main():
    last_uf_known_date = date(2023, 1, 9)  # Must be day 9
    last_uf_value = 28000.0
    new_ipc = 0.5  # IPC variation as a percentage

    # Call the get_ufs function and print its return value
    ufs = get_ufs(last_uf_known_date, last_uf_value, new_ipc)
    for date_key, uf_value in ufs.items():
        print(f"{date_key}: {uf_value}")

if __name__ == "__main__":
    main()
