"""Validación, limpieza, reporte y guardado de resultados."""
import csv
import math
import re
import statistics

from modelo import Paciente

PATRON_CODIGO = re.compile(r"PAC-\d{3}")

# Campo del registro -> (nombre legible, mínimo, máximo)
RANGOS = {
    "edad": ("edad", 18, 100),
    "imc": ("imc", 12, 60),
    "presion_sistolica": ("presión sistólica", 70, 250),
}
GRUPOS_VALIDOS = ("A", "B")


def convertir_numero(valor):
    """Devuelve float(valor), o None si el dato falta (None, '' o solo espacios).

    Si el valor no representa un número, float lanza ValueError.
    """
    if valor is None:
        return None
    if isinstance(valor, str) and valor.strip() == "":
        return None
    return float(valor)


def validar_registro(registro):
    """Devuelve la lista de motivos de rechazo (vacía si el registro es válido).

    No comprueba duplicados: eso requiere conocer los registros anteriores.
    """
    motivos = []

    codigo = registro.get("codigo")
    if not isinstance(codigo, str) or PATRON_CODIGO.fullmatch(codigo) is None:
        motivos.append("código con formato inválido")

    for campo, (nombre, minimo, maximo) in RANGOS.items():
        try:
            numero = convertir_numero(registro.get(campo))
        except (ValueError, TypeError):
            motivos.append(f"valor no numérico en {nombre}")
            continue
        if numero is None:
            motivos.append(f"{nombre} faltante")
        elif not math.isfinite(numero) or not minimo <= numero <= maximo:
            motivos.append(f"{nombre} fuera de rango ({minimo} a {maximo})")

    if registro.get("grupo") not in GRUPOS_VALIDOS:
        motivos.append("grupo inválido")

    return motivos


def limpiar(registros):
    """Devuelve (validos, rechazos) sin modificar la lista recibida.

    validos: lista de Paciente. Ante códigos repetidos se conserva la primera aparición.
    rechazos: lista de {"fila": n (desde 1), "codigo": ..., "motivo": ...}.
    """
    validos = []
    rechazos = []
    codigos_aceptados = set()

    for fila, registro in enumerate(registros, start=1):
        motivos = validar_registro(registro)
        if registro.get("codigo") in codigos_aceptados:
            motivos.append("código duplicado")

        if motivos:
            rechazos.append(
                {"fila": fila, "codigo": registro.get("codigo"), "motivo": "; ".join(motivos)}
            )
            continue

        codigos_aceptados.add(registro["codigo"])
        validos.append(
            Paciente(
                registro["codigo"],
                float(registro["edad"]),
                float(registro["imc"]),
                float(registro["presion_sistolica"]),
                registro["grupo"],
            )
        )
    return validos, rechazos


def _resumir(clave, pacientes):
    hipertensos = sum(1 for p in pacientes if p.es_hipertenso())
    return {
        "grupo": clave,
        "cantidad": len(pacientes),
        "presion_media": round(statistics.mean(p.presion for p in pacientes), 2),
        "proporcion_hipertensos": round(hipertensos / len(pacientes), 3),
    }


def generar_reporte(pacientes):
    """Una fila por grupo (ordenada). Con lista vacía devuelve una lista vacía."""
    por_grupo = {}
    for p in pacientes:
        por_grupo.setdefault(p.grupo, []).append(p)
    return [_resumir(grupo, por_grupo[grupo]) for grupo in sorted(por_grupo)]


def reporte_por_franja(pacientes):
    """Desafío adicional: igual que generar_reporte, agrupando por franja etaria."""
    por_franja = {}
    for p in pacientes:
        por_franja.setdefault(p.franja_etaria(), []).append(p)
    filas = []
    for franja in sorted(por_franja):
        fila = _resumir(franja, por_franja[franja])
        filas.append({"franja": fila.pop("grupo"), **fila})
    return filas


def guardar_csv(filas, ruta):
    """Guarda una lista (no vacía) de diccionarios; encabezados = claves de la primera fila."""
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)
