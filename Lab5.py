import random
from tabulate import tabulate


# Константи та параметри алгоритму
NUM_LESSONS = 23  # Кількість уроків на тиждень
NUM_SUBJECTS = 6  # Кількість різних уроків
NUM_TEACHERS = 3  # Кількість різних вчителів
NUM_CLASSES = 2  # Кількість класів
MAX_LESSONS_PER_DAY = 5  # Максимальна кількість уроків на день
NUM_SPECIAL_ROOMS = 1  # Кількість спеціалізованих приміщень

POPULATION_SIZE = 50  # Розмір початкової популяції
MAX_GENERATIONS = 100  # Максимальна кількість поколінь
CROSSOVER_RATE = 0.8  # Ймовірність схрещування
MUTATION_RATE = 0.2  # Ймовірність мутації

# Списки даних
lessons = ['Lesson{}'.format(i) for i in range(NUM_SUBJECTS)]
teachers = ['Teacher{}'.format(i) for i in range(NUM_TEACHERS)]
classes = ['Class{}'.format(i) for i in range(NUM_CLASSES)]
rooms = ['Room{}'.format(i) for i in range(NUM_CLASSES + NUM_SPECIAL_ROOMS)]


# Генерація випадкового розкладу занять
def generate_schedule():
    schedule = []
    for day in range(5):  # 5 робочих днів
        daily_schedule = []
        for _ in range(MAX_LESSONS_PER_DAY):
            if len(daily_schedule) < NUM_LESSONS:
                lesson = random.choice(lessons)
                teacher = random.choice(teachers)
                classroom = random.choice(rooms)
                daily_schedule.append((lesson, teacher, classroom))
            else:
                daily_schedule.append(None)  # Вікно (пропуск уроку)
        schedule.append(daily_schedule)
    return schedule


# Обчислення фітнес-функції (оцінки якості розкладу)
def calculate_fitness(schedule):
    fitness = 0
    for day in schedule:
        for lesson in day:
            if lesson:
                fitness += 1  # Збільшуємо фітнес за кожний заповнений урок
    return fitness


# Схрещування (одноточковий кросовер)
def crossover(parent1, parent2):
    crossover_point = random.randint(1, NUM_LESSONS - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child


# Мутація (заміна випадкового уроку)
def mutate(schedule):
    day = random.randint(0, 4)
    lesson = random.randint(0, MAX_LESSONS_PER_DAY - 1)
    new_lesson = (random.choice(lessons), random.choice(teachers), random.choice(rooms))
    schedule[day][lesson] = new_lesson
    return schedule


# Генетичний алгоритм оптимізації розкладу занять
def genetic_algorithm():
    # Ініціалізація початкової популяції
    population = [generate_schedule() for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        # Оцінка фітнес-функції для кожного розкладу
        fitness_scores = [calculate_fitness(schedule) for schedule in population]

        # Вибір найкращих розкладів для схрещування
        selected_parents = random.choices(population, weights=fitness_scores, k=POPULATION_SIZE // 2)

        # Створення нової популяції
        new_population = []
        for parent1, parent2 in zip(selected_parents[::2], selected_parents[1::2]):
            if random.random() < CROSSOVER_RATE:
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
            else:
                child1 = parent1
                child2 = parent2
            new_population.append(child1)
            new_population.append(child2)

            # Мутація в новій популяції
        for i in range(len(new_population)):
            if random.random() < MUTATION_RATE:
                new_population[i] = mutate(new_population[i])

                # Заміна старої популяції новою
        population = new_population

        # Вибір найкращого розкладу
    best_schedule = max(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_schedule)

    return best_schedule, best_fitness


# Запуск генетичного алгоритму та отримання найкращого розкладу
best_schedule, best_fitness = genetic_algorithm()

# Підготовка даних для таблиці
table_data = []
for day, daily_schedule in enumerate(best_schedule):
    table_row = ["День {}".format(day + 1)]
    for lesson in daily_schedule:
        if lesson:
            table_row.append(str(lesson))
        else:
            table_row.append("Вікно (пропуск уроку)")
    table_data.append(table_row)
table_data.append(["Оцінка якості розкладу:", str(best_fitness)])

# Виведення таблиці
table_headers = ["День", "Урок 1", "Урок 2", "Урок 3", "Урок 4", "Урок 5"]
table = tabulate(table_data, headers=table_headers, tablefmt="grid")
print(table)