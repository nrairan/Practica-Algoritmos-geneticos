# %% [markdown]
# # Ejercicio 1 - Maximización de f(x) = x³ - 4x² + 5x

# %%
import random
import math
import copy
import numpy as np
import matplotlib.pyplot as plt

random.seed(42)
np.random.seed(42)


# %%
class AlgoritmoGenetico:
    """
    Algoritmo Genético Canónico genérico y parametrizable.

    Opera sobre genotipos binarios (listas de 0s y 1s). La interpretación
    del genotipo como una solución real del problema (fenotipo) se delega
    por completo a `decode_func`, y su calidad se mide con `fitness_func`.
    Esto permite reutilizar la misma clase para distintos problemas de
    optimización sin modificar su lógica interna.

    Parámetros:
        population_size: Número de individuos por generación.
        chromosome_length: Cantidad de bits por cromosoma. Define la
            precisión de la decodificación (a mayor longitud, más
            resolución en el espacio de búsqueda).
        pc: Probabilidad de cruzamiento (0 a 1).
        pm: Probabilidad de mutación por bit (0 a 1).
        fitness_func: Función que recibe un fenotipo y devuelve su aptitud.
        decode_func: Función que convierte un genotipo binario en fenotipo.
        selection_method: 'roulette' (proporcional al fitness) o
            'tournament' (competencia entre individuos aleatorios).
        elitism: Si True, garantiza que el mejor individuo histórico
            sobreviva a la siguiente generación.
        tournament_size: Número de competidores por torneo (solo aplica
            si selection_method='tournament').
    """

    def __init__(
        self,
        population_size: int,
        chromosome_length: int,
        pc: float,
        pm: float,
        fitness_func: callable,
        decode_func: callable,
        selection_method: str = 'roulette',
        elitism: bool = True,
        tournament_size: int = 3,
    ):
        if not (0 <= pc <= 1 and 0 <= pm <= 1):
            raise ValueError("pc y pm deben estar entre 0 y 1.")
        if population_size <= 0 or chromosome_length <= 0:
            raise ValueError("population_size y chromosome_length deben ser positivos.")
        if selection_method not in ['roulette', 'tournament']:
            raise ValueError("selection_method debe ser 'roulette' o 'tournament'.")

        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.pc = pc
        self.pm = pm
        self.elitism = elitism
        self.fitness_func = fitness_func
        self.decode_func = decode_func
        self.selection_method = selection_method
        self.tournament_size = tournament_size

        self.population: list[list[int]] = []
        self.max_fitness_history: list[float] = []
        self.avg_fitness_history: list[float] = []
        self.best_individual_genotype: list[int] = []
        self.best_individual_fitness: float = -float('inf')

    def _initialize_population(self) -> None:
        """Genera la población inicial con cromosomas binarios aleatorios."""
        self.population = [
            [random.randint(0, 1) for _ in range(self.chromosome_length)]
            for _ in range(self.population_size)
        ]

    def _calculate_all_fitness(self, population: list[list[int]]) -> tuple[list[float], list]:
        """Decodifica y evalúa el fitness de cada individuo de la población."""
        fitness_values = []
        phenotypes = []
        for chromosome in population:
            phenotype = self.decode_func(chromosome)
            fitness = self.fitness_func(phenotype)
            fitness_values.append(fitness)
            phenotypes.append(phenotype)
        return fitness_values, phenotypes

    def _select_proportional(self, population: list[list[int]], fitness_values: list[float]) -> [list[int]]:
        """
        Selección por ruleta: probabilidad de ser elegido proporcional al fitness.
        Si hay valores negativos, se desplazan para que todos sean >= 0
        antes de calcular las probabilidades.
        """
        min_fitness = min(fitness_values)
        if min_fitness < 0:
            adjusted_fitness = [f - min_fitness + 1e-6 for f in fitness_values]
        else:
            adjusted_fitness = fitness_values

        total_fitness = sum(adjusted_fitness)

        if total_fitness == 0:
            return random.choices(population, k=self.population_size)

        selection_probabilities = [f / total_fitness for f in adjusted_fitness]
        new_population = random.choices(population, weights=selection_probabilities, k=self.population_size)
        return new_population

    def _select_tournament(self, population: list[list[int]], fitness_values: list[float]) -> list[list[int]]:
        """Selección por torneo: elige al mejor entre `tournament_size` individuos aleatorios."""
        new_population = []
        for _ in range(self.population_size):
            tournament_contestants_indices = random.sample(range(self.population_size), self.tournament_size)

            best_contestant_index = tournament_contestants_indices[0]
            for i in tournament_contestants_indices:
                if fitness_values[i] > fitness_values[best_contestant_index]:
                    best_contestant_index = i
            new_population.append(copy.deepcopy(population[best_contestant_index]))
        return new_population

    def _crossover_one_point(self, parent1: list[int], parent2: list[int]) -> tuple[list[int], list[int]]:
        """Cruce de un punto: intercambia segmentos entre dos padres con probabilidad `pc`."""
        if random.random() < self.pc:
            point = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        else:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)

    def _mutate_flip_bit(self, chromosome: list[int]) -> list[int]:
        """Invierte cada bit del cromosoma con probabilidad `pm`."""
        mutated_chromosome = copy.deepcopy(chromosome)
        for i in range(self.chromosome_length):
            if random.random() < self.pm:
                mutated_chromosome[i] = 1 - mutated_chromosome[i]
        return mutated_chromosome

    def _apply_elitism(self, new_population: list[list[int]]) -> list[list[int]]:
        """Reemplaza al peor individuo de la nueva generación por el mejor histórico."""
        if not self.best_individual_genotype:
            return new_population

        new_fitness_values, _ = self._calculate_all_fitness(new_population)
        worst_individual_index = np.argmin(new_fitness_values)

        new_population[worst_individual_index] = copy.deepcopy(self.best_individual_genotype)
        return new_population

    def run(self, num_generations: int) -> tuple[list[int], float]:
        """
        Ejecuta el ciclo completo del AG: evaluación, selección, cruce,
        mutación y elitismo, durante `num_generations` iteraciones.

        Retorna el mejor genotipo encontrado y su fitness.
        """
        self._initialize_population()

        for generation in range(num_generations):
            fitness_values, _ = self._calculate_all_fitness(self.population)

            current_best_index = np.argmax(fitness_values)
            current_best_fitness = fitness_values[current_best_index]
            current_best_genotype = copy.deepcopy(self.population[current_best_index])

            if current_best_fitness > self.best_individual_fitness:
                self.best_individual_fitness = current_best_fitness
                self.best_individual_genotype = current_best_genotype

            self.max_fitness_history.append(self.best_individual_fitness)
            self.avg_fitness_history.append(np.mean(fitness_values))

            if self.selection_method == 'roulette':
                mating_pool = self._select_proportional(self.population, fitness_values)
            else:
                mating_pool = self._select_tournament(self.population, fitness_values)

            new_population = []
            if len(mating_pool) % 2 != 0:
                mating_pool.append(random.choice(mating_pool))

            random.shuffle(mating_pool)

            for i in range(0, self.population_size, 2):
                parent1 = mating_pool[i]
                parent2 = mating_pool[i + 1]

                child1, child2 = self._crossover_one_point(parent1, parent2)

                child1 = self._mutate_flip_bit(child1)
                child2 = self._mutate_flip_bit(child2)

                new_population.extend([child1, child2])

            self.population = new_population[:self.population_size]

            if self.elitism:
                self.population = self._apply_elitism(self.population)

        return self.best_individual_genotype, self.best_individual_fitness


# %% [markdown]
# ## Ejercicio 1: f(x) = x³ - 4x² + 5x
#
# f'(x) = 3x² - 8x + 5 = 0 → x = 1 (máximo local) o x = 5/3 (mínimo local).
#
# Nota: dentro del rango [-1, 3], f(3) = 6 es mayor que f(1) = 2, por lo que
# el AG converge al borde x=3 (máximo global en ese dominio), no al máximo
# local x=1. Para forzar la convergencia al máximo local, acotar el rango
# a X_MAX_EJ1 < 2 (ej. 1.9).

# %%
X_MIN_EJ1, X_MAX_EJ1 = -1, 3   # Rango de búsqueda del fenotipo x
N_BITS_EJ1 = 8                 # Bits del cromosoma: 2^8 = 256 puntos de resolución


def decode_cubic(genotype: list[int]) -> float:
    """Mapea un genotipo binario a un valor real x en [X_MIN_EJ1, X_MAX_EJ1]."""
    entero = int("".join(str(bit) for bit in genotype), 2)
    max_entero = 2**len(genotype) - 1
    return X_MIN_EJ1 + (entero / max_entero) * (X_MAX_EJ1 - X_MIN_EJ1)


def fitness_cubic(x: float) -> float:
    """Función objetivo a maximizar: f(x) = x³ - 4x² + 5x."""
    return x**3 - 4*x**2 + 5*x


# Parámetros del AG
POP_SIZE_EJ1 = 20
PC_EJ1 = 0.8            # Probabilidad de cruce
PM_EJ1 = 0.1            # Probabilidad de mutación por bit
NUM_GENERATIONS_EJ1 = 50

print("\n--- Ejecutando AG para f(x) = x³ - 4x² + 5x (Ejercicio 1) ---")

cubic_ga = AlgoritmoGenetico(
    population_size=POP_SIZE_EJ1,
    chromosome_length=N_BITS_EJ1,
    pc=PC_EJ1,
    pm=PM_EJ1,
    fitness_func=fitness_cubic,
    decode_func=decode_cubic,
    selection_method='roulette',
    elitism=True,
)

final_best_genotype_ej1, final_best_fitness_ej1 = cubic_ga.run(NUM_GENERATIONS_EJ1)
final_best_x_ej1 = decode_cubic(final_best_genotype_ej1)

print(f"\n--- Resultados Finales Ejercicio 1 ---")
print(f"Mejor Genotipo: {''.join(map(str, final_best_genotype_ej1))}")
print(f"Mejor x encontrado: {final_best_x_ej1:.4f}")
print(f"Mejor f(x): {final_best_fitness_ej1:.4f}")


# %% [markdown]
# ### Curva de convergencia

# %%
plt.figure(figsize=(8, 5))
plt.plot(range(1, NUM_GENERATIONS_EJ1 + 1), cubic_ga.max_fitness_history, label='Fitness Máximo')
plt.plot(range(1, NUM_GENERATIONS_EJ1 + 1), cubic_ga.avg_fitness_history, label='Fitness Promedio')
plt.title('Convergencia del AG: f(x) = x³ - 4x² + 5x')
plt.xlabel('Generación')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)
plt.show()