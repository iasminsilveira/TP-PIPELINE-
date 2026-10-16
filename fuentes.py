"""Fuentes de datos: interfaz común y dos implementaciones (CSV y JSON)."""
import csv
import json
from abc import ABC, abstractmethod


class FuenteDatos(ABC):
    """Interfaz común: toda fuente devuelve una lista de diccionarios."""

    @abstractmethod
    def cargar(self, ruta):
        """Lee el archivo y devuelve una lista de diccionarios (un registro cada uno)."""


class FuenteCSV(FuenteDatos):
    """Lee un CSV. Todos los valores se devuelven como texto."""

    def cargar(self, ruta):
        with open(ruta, encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))


class FuenteJSON(FuenteDatos):
    """Lee un JSON cuyo contenido debe ser una lista de registros."""

    def cargar(self, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, list):
            raise ValueError(
                f"El JSON debe contener una lista de registros, "
                f"pero contiene un objeto de tipo {type(datos).__name__}"
            )
        return datos
