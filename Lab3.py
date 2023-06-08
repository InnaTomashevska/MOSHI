import random
import matplotlib.pyplot as plt
import numpy as np

#генерує випадкову точку з координатами у проміжку [0,1] і додає її до списку `point`
def pointCreate(points):
    return points.append([random.uniform(0, 1), random.uniform(0, 1)])

#генерує суму випадкових точок у просторі
def pointSpaceFill(amount):
    points = []
    while amount > len(points):
        pointCreate(points)
    return points

#обчислює відстань між двома точками у просторі за допомогою формули відстані між точками
def measureCalculating(firstX, firstY, secondX, secondY):
    return np.sqrt((secondX - firstX) ** 2 + (secondY - firstY) ** 2)

#порівнює відстані між точкою та центрами кластерів та повертає індекс найближчого кластера
def comparisonClusters(measures):
    min_value, index = measures[0], 0
    for i in range(len(measures)):
        if measures[i] < min_value:
            min_value = measures[i]
            index = i
    return index

def clustering(points, centers, amount, clusterAmount):
    clusters, num = [[] for i in range(clusterAmount)], 0
    while num < amount:
        measures = []
        for i in range(clusterAmount):
            measures.append(measureCalculating(points[num][0], points[num][1], centers[i][0], centers[i][1]))
        clusters[comparisonClusters(measures)].append(points[num])
        num += 1
    return clusters

#Знаходить новий центр кластера шляхом обчислення середньої координати всіх точок у кластері
def newCenterFindingMeans(cluster):
    sumX, sumY = 0, 0
    for i in range(len(cluster)):
        sumX += cluster[i][0]
        sumY += cluster[i][1]
    return [sumX / len(cluster), sumY / len(cluster)]

def kMeansClustering(points, clusterAmount):
    N = len(points)
    clusterCenters = [points[random.randint(0, N - 1)] for _ in range(clusterAmount)]

    while True:
        clusters = clustering(points, clusterCenters, N, clusterAmount)
        newCenters = [newCenterFindingMeans(cluster) for cluster in clusters]

        if newCenters == clusterCenters:
            break

        clusterCenters = newCenters

    return clusters, clusterCenters

def hierarchicalClustering(points, clusterAmount):
    N = len(points)
    clusterCenters = [points[random.randint(0, N - 1)] for _ in range(clusterAmount)]

    while True:
        clusters = clustering(points, clusterCenters, N, clusterAmount)
        newCenters = [newCenterFindingMeans(cluster) for cluster in clusters]

        if newCenters == clusterCenters:
            break

        clusterCenters = newCenters

    return clusters, clusterCenters

#Візуалізує кластери
def createClusteringGraph(clusters, centers, title):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.set_title(title, fontsize=18)
    plt.grid(True)
    colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))

    for i in range(len(clusters)):
        cluster_color = colors[i]
        for j in range(len(clusters[i])):
            ax.scatter(clusters[i][j][0], clusters[i][j][1], color=cluster_color, s=10)
        ax.scatter(centers[i][0], centers[i][1], color='black', marker='o', s=100)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.show()

N, K = 1000, 5

pointSpace = pointSpaceFill(N)

kMeansClusters, kMeansClusterCenters = kMeansClustering(pointSpace, K)
hierarchicalClusters, hierarchicalClusterCenters = hierarchicalClustering(pointSpace, K)

createClusteringGraph(kMeansClusters, kMeansClusterCenters, "K-середніх")
createClusteringGraph(hierarchicalClusters, hierarchicalClusterCenters, "Ієрархічний метод")
