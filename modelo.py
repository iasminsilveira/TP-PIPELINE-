"""Clase del dominio: un paciente con una medición ya validada."""


class Paciente:
    """Registro validado: atributos numéricos float y grupo 'A' o 'B'."""

    # Criterio didáctico simplificado, no es un diagnóstico clínico.
    UMBRAL_HIPERTENSION = 140.0  # mmHg

    def __init__(self, codigo, edad, imc, presion, grupo):
        self.codigo = codigo
        self.edad = edad
        self.imc = imc
        self.presion = presion
        self.grupo = grupo

    def franja_etaria(self):
        if self.edad < 40:
            return "18-39"
        if self.edad < 60:
            return "40-59"
        return "60+"

    def es_hipertenso(self):
        return self.presion >= self.UMBRAL_HIPERTENSION

    def __str__(self):
        return (
            f"{self.codigo} | grupo {self.grupo} | {self.edad:.0f} años "
            f"| PAS {self.presion:.0f} mmHg"
        )
