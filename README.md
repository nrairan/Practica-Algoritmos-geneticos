# Ejercicio 3 - Análisis de la Tasa de Mutación

## Objetivo

Analizar la velocidad y calidad de la convergencia del Algoritmo Genético al variar únicamente la probabilidad de mutación (pm = 0.01, 0.1 y 0.5), manteniendo constantes los demás parámetros del problema.

## Enfoque

* **Codificación:** cromosomas de 16 bits, decodificados a un valor real x en el rango [-1, 2].
* **Fitness:** el valor directo de f(x) (problema de maximización).
* **Selección:** torneo de tamaño 3.
* **Cruce:** un punto, con pc = 0.8.
* **Mutación:** bit a bit, evaluando pm = 0.01, pm = 0.1 y pm = 0.5.
* **Elitismo:** activado (preserva al mejor individuo de la población).
* **Control:** uso de la misma semilla aleatoria (seed = 42) para garantizar condiciones iniciales idénticas en todas las ejecuciones.

## Resultado esperado

* **pm = 0.01 (mutación baja):** convergencia rápida pero con riesgo de estancamiento en óptimos locales por falta de diversidad genética.
* **pm = 0.1 (mutación moderada):** equilibrio óptimo entre exploración del espacio de búsqueda y explotación de las mejores soluciones.
* **pm = 0.5 (mutación alta):** comportamiento errático similar a una búsqueda aleatoria, lo que dificulta la estabilización en la solución óptima.

## Archivos

ejercicio_3.py / ejercicio_3.ipynb: implementación completa que incluye la comparación de las tres tasas de mutación y la gráfica superpuesta de sus curvas de convergencia.

---

# Ejercicio 4 - Elitismo Ampliado

## Objetivo

Evaluar el impacto en la estabilidad y velocidad de convergencia al modificar el mecanismo de elitismo para preservar de forma intacta a los 3 mejores individuos de cada generación hacia la siguiente.

## Enfoque

* **Codificación:** cromosomas de 16 bits, decodificados a un valor real x en el rango [-1, 2].
* **Fitness:** el valor directo de f(x) (problema de maximización).
* **Selección:** torneo de tamaño 3.
* **Cruce:** un punto, con pc = 0.8.
* **Mutación:** bit a bit, con pm = 0.1.
* **Elitismo:** comparación entre elitismo clásico (1 individuo) y elitismo ampliado (k = 3 individuos intactos).

## Resultado esperado

Preservar a los 3 mejores individuos acelera la convergencia hacia el máximo global (x = 1, f(1) = 2) y previene la pérdida de material genético de alta calidad frente a los efectos destructivos del cruce o la mutación. Sin embargo, un elitismo excesivo incrementa el riesgo de dominancia prematura por parte de unos pocos individuos aptos.

## Archivos

ejercicio_4.py / ejercicio_4.ipynb: implementación completa que incluye la comparación de convergencia entre elitismo clásico (k = 1) y elitismo ampliado (k = 3) con su respectiva gráfica.