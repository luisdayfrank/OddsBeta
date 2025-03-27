import os
from pathlib import Path
# Configuraciones globales
FILE_PATH = 'libro2.xlsx'
DATABASE_PATH = 'base_datos_analisisv3.xlsx'
ROUND_WEIGHTS = {'R128': 1, 'R64': 1.2, 'R32': 1.5, 'QF': 2, 'SF': 2.5, 'F': 3}
DATA_DIR = Path('datos')  # Carpeta para copias de seguridad
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Crear si no existe
backup_dir = Path('datos')  # Nueva configuración para copias