"""Punto de entrada. Uso: python src/main.py data/mediciones.csv  (o .json)"""
import sys
from pathlib import Path

from fuentes import FuenteCSV, FuenteJSON
from pipeline import limpiar, generar_reporte, guardar_csv

CARPETA_SALIDA = Path("outputs")
FUENTES = {".csv": FuenteCSV, ".json": FuenteJSON}


def elegir_fuente(ruta):
    extension = Path(ruta).suffix.lower()
    if extension not in FUENTES:
        raise ValueError(
            f"Extensión '{extension}' no soportada. Use una de: {', '.join(FUENTES)}"
        )
    return FUENTES[extension]()


def main(ruta_entrada):
    registros = elegir_fuente(ruta_entrada).cargar(ruta_entrada)
    validos, rechazos = limpiar(registros)
    reporte = generar_reporte(validos)

    print(f"Leídos: {len(registros)} | válidos: {len(validos)} | rechazados: {len(rechazos)}")
    for fila in reporte:
        print(fila)

    CARPETA_SALIDA.mkdir(exist_ok=True)
    if reporte:
        guardar_csv(reporte, CARPETA_SALIDA / "reporte.csv")
    if rechazos:
        guardar_csv(rechazos, CARPETA_SALIDA / "rechazos.csv")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python src/main.py <archivo_de_mediciones.csv|.json>")
    main(sys.argv[1])
