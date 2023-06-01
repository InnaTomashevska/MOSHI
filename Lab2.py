import numpy as math
from scipy import integrate
import random
import matplotlib.pyplot as plot

# Функція для тестування
def testFunction(x):
    return math.sin(x)

# Основна функція
def mainFunction(x):
    return math.exp(x ** 2)

# Функція для обчислення інтеграла функції на відрізку
def functionIntegrate(function, start, end):
    square = integrate.quad(function, start, end)
    return square[0]

# Функція для обчислення значення функції
def valueCalculate(value, flag):
    return testFunction(value) if flag == 0 else mainFunction(value)

# Функція для створення випадкової точки
def pointCreate(startX, endX, startY, endY):
    return [random.uniform(startX, endX), random.uniform(startY, endY)]

# Функція для знаходження меж по осі Y
def YLimitsFinding(startX, endX, identifier, step):
    maxY, minY = valueCalculate(startX, identifier), valueCalculate(startX, identifier)
    presentX, presentY = startX, valueCalculate(startX, identifier)
    while presentX < endX:
        presentY = valueCalculate(presentX, identifier)
        maxY = max(maxY, presentY)
        minY = min(minY, presentY)
        presentX += step
    return [math.floor(minY), math.round(maxY)]

# Функція для обчислення кількості точок, що потрапляють в область під кривою
def squarePointsCalculate(points, identifier):
    amount = 0
    for i in range(len(points)):
        if valueCalculate(points[i][0], identifier) > points[i][1]:
            amount += 1
    return amount

# Функція для створення графіку
def graphCreate(points, startX, endX, startY, endY, identifier):
    graph, ax = plot.subplots(1, 1, figsize=(5, 5))
    plot.grid(True)
    x = math.linspace(startX, endX)
    plot.plot(x, valueCalculate(x, identifier), linewidth=3, color="black", label='Графік функції')
    for i in range(len(points)):
        if valueCalculate(points[i][0], identifier) > points[i][1]:
            ax.scatter(points[i][0], points[i][1], color='red', s=10)
        else:
            ax.scatter(points[i][0], points[i][1], color='green', s=10)
    plot.xlim(startX - identifier, endX + identifier)
    plot.ylim(startY - identifier, endY + identifier)
    plot.legend()
    plot.show()

# Функція для виведення результатів
def messagePrint(trueSquare, square, absoluteError):
    print("Значення площі: ", "\t"*5, trueSquare)
    print("Значення площі методом Монте-Карло: \n", square)
    print("Абсолютна похибка: ", "\t"*5, math.round(absoluteError, 5))
    print("Відносна похибка: ", "\t"*5, math.round(absoluteError / trueSquare * 100, 5), "\b%")

testX, mainX = [0, 1], [0, 1]
iterations, pointSpaceMain, pointSpaceTest = 1000, [], []

# Знаходимо межі для тестової та основної функції
testY, mainY = YLimitsFinding(testX[0], testX[1], 0, 0.1), YLimitsFinding(mainX[0], mainX[1], 1, 0.001)

# Генеруємо випадкові точки
for i in range(iterations):
    pointSpaceMain.append(pointCreate(mainX[0], mainX[1], mainY[0], mainY[1]))
    pointSpaceTest.append(pointCreate(testX[0], testX[1], testY[0], testY[1]))

# Створюємо графіки для тестової та основної функцій
graphCreate(pointSpaceMain, mainX[0], mainX[1], mainY[0], mainY[1], 1)
graphCreate(pointSpaceTest, testX[0], testX[1], testY[0], testY[1], 0)

# Обчислюємо кількість точок, що потрапляють під криву
squarePointsTest, squarePointsMain = squarePointsCalculate(pointSpaceTest, 0), squarePointsCalculate(pointSpaceMain, 1)

# Обчислюємо площу
squareTest = (testY[1] - testY[0]) * (testX[1] - testX[0]) * (squarePointsTest / iterations)
squareMain = (mainY[1] - mainY[0]) * (mainX[1] - mainX[0]) * (squarePointsMain / iterations)

# Обчислюємо точне значення площі
trueSquareTest, trueSquareMain = functionIntegrate(testFunction, testX[0], testX[1]), functionIntegrate(mainFunction, mainX[0], mainX[1])

# Обчислюємо похибку
absoluteErrorTest, absoluteErrorMain = math.absolute(trueSquareTest - squareTest), math.absolute(trueSquareMain - squareMain)

print("\nТестова функція:\n")
messagePrint(trueSquareTest, squareTest, absoluteErrorTest)
print("\n\nОсновна функція:\n")
messagePrint(trueSquareMain, squareMain, absoluteErrorMain)