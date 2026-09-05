# Ejercicio 1 - Maximización Cúbica

## Objetivo

Encontrar el valor de `x` que maximiza la función:

```
f(x) = x³ - 4x² + 5x
```

usando un Algoritmo Genético con codificación binaria.

## Enfoque

- **Codificación:** cromosomas de 8 bits, decodificados a un valor real `x` en el rango `[-1, 3]`.
- **Fitness:** el valor directo de `f(x)` (problema de maximización).
- **Selección:** ruleta proporcional al fitness.
- **Cruce:** un punto, con `pc = 0.8`.
- **Mutación:** bit a bit, con `pm = 0.1`.
- **Elitismo:** activado (preserva al mejor individuo entre generaciones).

## Resultado esperado

`f'(x) = 3x² - 8x + 5 = 0` tiene raíces en `x = 1` (máximo local) y `x = 5/3` (mínimo local). Sin embargo, dentro del rango `[-1, 3]`, `f(3) = 6` supera a `f(1) = 2`, por lo que el AG converge correctamente al **máximo global del dominio en x = 3**, no al máximo local.

Para observar convergencia al máximo local (`x = 1`), acotar el rango a `X_MAX < 2`.

## Archivos

- `ejercicio1.py` / `ejercicio1.ipynb`: implementación completa, incluyendo la clase `AlgoritmoGenetico` y la gráfica de convergencia (fitness máximo y promedio por generación).

# Ejercicio 2 - Optimización Multivariable

## Objetivo

Encontrar el par `(x, y)` que minimiza la función:

```
f(x, y) = x² + y²
```

usando un Algoritmo Genético con codificación binaria y dos variables.

## Enfoque

- **Codificación:** cromosomas de 8 bits, divididos en dos mitades: los primeros 4 bits decodifican `x`, los últimos 4 decodifican `y`. Ambas variables se mapean al rango `[-5, 5]`.
- **Fitness:** como la clase `AlgoritmoGenetico` siempre maximiza, se minimiza `f(x,y)` maximizando su negativo: `fitness = -(x² + y²)`.
- **Selección:** ruleta proporcional al fitness.
- **Cruce:** un punto, con `pc = 0.8`.
- **Mutación:** bit a bit, con `pm = 0.1`.
- **Elitismo:** activado.

## Resultado esperado

El mínimo global de `f(x,y) = x² + y²` está en `(x, y) = (0, 0)`, con `f(0,0) = 0`. El AG debe converger a valores de `x` e `y` cercanos a cero conforme avanzan las generaciones.

## Archivos

- `ejercicio2.py` / `ejercicio2.ipynb`: implementación completa, incluyendo la clase `AlgoritmoGenetico`, la decodificación multivariable y la gráfica de convergencia (expresada en términos de `f(x,y)` real, no del fitness negado).