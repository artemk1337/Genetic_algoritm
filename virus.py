import numpy as np
import matplotlib.pyplot as plt


# указав размер для каждого и
# каждый сюжет matplotlib по всему миру
plt.rcParams['figure.figsize'] = [8, 6]


# определение вируса в виде массива numy
virus = np.array([0, 0])


# пустой список объектов для хранения населения
population = []
# определение объектов списка с диапазоном графика
x1_range = [-100, 100]
x2_range = [-100, 100]


# Создает популяцию
# features - массив с диапозонами
def populate(features, size=1000):
    # здесь мы определяем координату
    # для каждого субъекта в популяции
    initial = []
    for _ in range(size):
        entity = []
        for feature in features:
            # this * переменная функции распаковывает список
            # или кортеж в аргументах позиции.
            val = np.random.randint(*feature)
            entity.append(val)
        initial.append(entity)
        del entity
    return np.array(initial)


# Сколько подходящих выживут
def fitness(population, virus, size=100):
    scores = []
    # enumerate также предоставляет индекс как для итератора
    for index, entity in enumerate(population):
        score = np.sum((entity - virus) ** 2)
        scores.append((score, index))
    scores = sorted(scores)[:size]
    return np.array(scores)[:, 1]


# эта функция используется для построения графика
def draw(population, virus):
    plt.xlim((-100, 100))
    plt.ylim((-100, 100))
    plt.scatter(population[:, 0], population[:, 1], c='green', s=12)
    plt.scatter(virus[0], virus[1], c='red', s=60)
    plt.show()


def reduction(population, virus, size=100):
    # только индекс наиболее подходящих
    # возвращается в отсортированном формате
    fittest = fitness(population, virus, size)
    new_pop = []
    for item in fittest:
        new_pop.append(population[item])
    return np.array(new_pop)


# перекрестная мутация для генерации следующего поколения
# Количество населения, которое будет более защищено от вируса, чем предыдущие
def cross(population, size=1000):
    new_pop = []
    for _ in range(size):
        p = population[np.random.randint(0, len(population))]
        m = population[np.random.randint(0, len(population))]
        # мы рассматриваем только половину каждого
        # без учета случайного выбора
        entity = []
        entity.append(*p[:len(p) // 2])
        entity.append(*m[len(m) // 2:])
        new_pop.append(entity)
    return np.array(new_pop)


# генерация и добавление случайных объектов в
# сущность, чтобы она выглядела более распределенной
def mutate(population):
    return population + np.random.randint(-10, 10, 2000).reshape(1000, 2)


# gens - номер поколения
def cycle(population, virus, gens=1):
    # Создаем начальную популяцию
    population = populate([x1_range, x2_range], 1000)
    draw(population, virus)
    # А теперь улучшаем её
    for _ in range(gens):
        population = reduction(population, virus, 100)
        population = cross(population, 1000)
        # population = mutate(population)
        draw(population, virus)


cycle(population, virus, 5)

