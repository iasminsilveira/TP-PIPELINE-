# TP-PIPELINE-
# Pipeline de control de presión arterial

**Integrantes:** Silveira Fernández Iasmin - Ray Maria Alfonsina - Tacconi Constanza - Torres Clara

## Problema y usuario
Un equipo de salud recibe mediciones de presión arterial de un estudio en dos formatos (CSV y JSON) con errores de carga. El programa descarta los registros inválidos dejando constancia del motivo y resume la presión sistólica por grupo del estudio (A: control, B: intervención).

## Datos
Cada fila corresponde a un paciente con una medición.


## Ejecución
No requiere bibliotecas externas 


## Pruebas
Imprime `Todas las pruebas pasaron.` Cubren el caso normal, entradas inválidas y límites,
y propiedades del resultado (ningún registro se pierde, CSV y JSON dan el mismo reporte)

## Limitaciones
- Datos simulados y de tamaño reducido (50 pacientes válidos).
- Los registros con varios problemas se rechazan completos; no se intenta corregir valores.
