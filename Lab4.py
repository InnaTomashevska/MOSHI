import random
import numpy as np
import matplotlib.pyplot as plt

def generate_map(num_cities, min_distance, max_distance):
    map_data = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = random.randint(min_distance, max_distance)
            map_data[i][j] = distance
            map_data[j][i] = distance
    return map_data

def save_map(map_data, filename):
    np.savetxt(filename, map_data, delimiter=',')

def load_map(filename):
    return np.loadtxt(filename, delimiter=',')

def calculate_path_cost(path, map_data):
    num_cities = len(path)
    cost = 0
    for i in range(num_cities - 1):
        from_city = path[i]
        to_city = path[i+1]
        cost += map_data[from_city][to_city]
    cost += map_data[path[-1]][path[0]]  # Додати витрати на повернення до початкового міста
    return cost

def ant_colony_tsp(map_data, num_ants, evaporation_rate, alpha, beta, num_iterations):
    num_cities = len(map_data)
    pheromone = np.ones((num_cities, num_cities))  # Початкові рівні феромонів
    best_path = None
    best_cost = float('inf')
    best_paths = []  # Зберігатиме найкращі маршрути для кожної ітерації
    best_costs = []  # Зберігатиме найкращі вартості для кожної ітерації

    for iteration in range(num_iterations):
        # Кожна мурашка починає з випадкового міста
        ant_paths = []
        for ant in range(num_ants):
            start_city = random.randint(0, num_cities - 1)
            path = [start_city]
            available_cities = set(range(num_cities))
            available_cities.remove(start_city)

            while available_cities:
                current_city = path[-1]
                next_city = choose_next_city(current_city, available_cities, pheromone, map_data, alpha, beta)
                path.append(next_city)
                available_cities.remove(next_city)

            ant_paths.append(path)

        # Оновлення рівнів феромонів
        pheromone = update_pheromone(pheromone, ant_paths, evaporation_rate)

        # Знайти найкращий шлях в поточній ітерації
        for path in ant_paths:
            cost = calculate_path_cost(path, map_data)
            if cost < best_cost:
                best_cost = cost
                best_path = path

        best_paths.append(best_path)
        best_costs.append(best_cost)

    return best_paths, best_costs

def choose_next_city(current_city, available_cities, pheromone, map_data, alpha, beta):
    pheromone_values = pheromone[current_city, list(available_cities)]
    visibility_values = 1.0 / (map_data[current_city, list(available_cities)] + 1e-8)
    probabilities = np.power(pheromone_values, alpha) * np.power(visibility_values, beta)
    probabilities /= np.sum(probabilities)
    next_city = random.choices(list(available_cities), weights=probabilities)[0]
    return next_city

def update_pheromone(pheromone, ant_paths, evaporation_rate):
    pheromone *= (1 - evaporation_rate)  # Випаровування феромонів
    num_ants = len(ant_paths)
    for path in ant_paths:
        contribution = 1.0 / calculate_path_cost(path, map_data)
        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i+1]
            pheromone[from_city][to_city] += contribution
            pheromone[to_city][from_city] += contribution
    return pheromone

# Задані параметри
num_cities = random.randint(25, 35)
min_distance = 10
max_distance = 100
num_ants = 10
evaporation_rate = 0.5
alpha = 1
beta = 5
num_iterations = 10

# Згенерувати або завантажити карту маршрутів
map_filename = 'map.csv'
try:
    map_data = load_map(map_filename)
except IOError:
    map_data = generate_map(num_cities, min_distance, max_distance)
    save_map(map_data, map_filename)

# Виконати послідовність з 10 симуляцій
best_paths, best_costs = ant_colony_tsp(map_data, num_ants, evaporation_rate, alpha, beta, num_iterations)

# Вивести всі маршрути
for i, path in enumerate(best_paths):
    cost = best_costs[i]
    print(f'Iteration {i+1}: Path = {path}, Cost = {cost}')
    # Знайти найкращий маршрут і його вартість
    best_index = np.argmin(best_costs)
    best_path = best_paths[best_index]
    best_cost = best_costs[best_index]
    print(f'Best Path: {best_path}')
    print(f'Best Cost: {best_cost}')

    # Створити графік з усіма маршрутами
    plt.figure()
    for path in best_paths:
        x = [map_data[city][0] for city in path]
        y = [map_data[city][1] for city in path]
        plt.plot(x, y, marker='o')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ant Colony TSP - All Paths')

    # Зберегти графік з найкращим маршрутом
    x = [map_data[city][0] for city in best_path]
    y = [map_data[city][1] for city in best_path]
    plt.figure()
    plt.plot(x, y, 'r-', marker='o')
    plt.plot(x[0], y[0], 'go', label='Start')  # Додати початкову точку
    plt.plot(x[-1], y[-1], 'bo', label='End')  # Додати кінцеву точку
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ant Colony TSP - Best Path')
    plt.legend()  # Вивести легенду

    # Показати графіки
    plt.show()
