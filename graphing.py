import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json as js
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import pickle

clusterValueDict = {}  # key: no. of clusters; value: (centroids, varianceList, clusterAssignments(dict), loss)
with open('cvKIL_changed.json', 'r') as readcvK:
     clusterValueDict = js.load(readcvK)

trainingExamples_Dict = {}
with open('distance_changedIL.pkl', 'rb') as f:
    trainingExamples_Dict = pickle.load(f)
centroids, varianceList, clusterAssignments, loss = clusterValueDict['1']
SIZE = len(clusterAssignments)
print(SIZE)

trainingExamples = np.zeros((SIZE, SIZE))
for key in trainingExamples_Dict:
    x_value, y_value = key
    trainingExamples[x_value][y_value] = trainingExamples_Dict[key]
    trainingExamples[y_value][x_value] = trainingExamples_Dict[key]

#print(cross_validate_K['u'10''])

# This file will compute two graphs.

trainingLossDict = {} #for training loss - iterations: loss
testLossDict = {} #for test loss - iterations: loss


def plotOptimalKGraphElbow(clusterValueDict):
    A = [0] * len(clusterValueDict)
    B = [0] * len(clusterValueDict)
    for clusterNumber in clusterValueDict:
        centroids, varianceList, clusterAssignments, loss = clusterValueDict[clusterNumber]
        A[int(clusterNumber) - 1] = int(clusterNumber)
        B[int(clusterNumber) - 1] = loss
    plt.plot(A, B)
    plt.xlabel("clusterNumber")
    plt.ylabel("loss")
    plt.title("Elbow Graph")
    plt.show()

def plotSilhouette(clusterValueDict, trainingExamples):
    A = [0] * len(clusterValueDict)
    B = [0] * len(clusterValueDict)
    for clusterNumber in clusterValueDict:
        if int(clusterNumber) > 1:
            A[int(clusterNumber) - 1] = int(clusterNumber)
            centroids, varianceList, clusterAssignments_dict, loss = clusterValueDict[clusterNumber]
            clusterAssignments = np.zeros(SIZE)
            for i in clusterAssignments_dict:
                clusterAssignments[int(i)] = clusterAssignments_dict[i]
            print(clusterAssignments)
            print(clusterNumber)
            silhouette_avg = silhouette_score(trainingExamples, clusterAssignments, metric = "precomputed")
            print(silhouette_avg)
            B[int(clusterNumber) - 1] = silhouette_avg
    plt.plot(A, B)
    plt.xlabel("Cluster Number")
    plt.ylabel("Silhouette Average")
    plt.title("Silhouette Analysis")
    #plt.legend()
    plt.show()

def plotBiasVariance(trainingLossDict, testLossDict):
    A = []
    B = []
    for iterations in trainingLossDict:
        A.append(iterations)
        B.append(trainingLossDict.get(iterations))
    plt.plot(A, B, "Training")
    C = []
    D = []
    for iterations in testLossDict:
        A.append(iterations)
        B.append(testLossDict.get(iterations))
    plt.plot(C, D, "Test")
    plt.xlabel("Iterations")
    plt.ylabel("Loss")
    plt.title("Bias-Variance")
    plt.legend()
    plt.show()

def plotClusterVariance(clusterValueDict, trainingExamples):
    A = [0] * len(clusterValueDict)
    B = [0] * len(clusterValueDict)
    for clusterNumber in clusterValueDict:
        A[int(clusterNumber) - 1] = int(clusterNumber)
        centroids, varianceList, clusterAssignments, loss = clusterValueDict[clusterNumber]
        meanVariance = sum(varianceList.values())/float(len(varianceList.values()))
        B[int(clusterNumber) - 1] = meanVariance
    plt.plot(A, B)
    plt.xlabel("Cluster Number")
    plt.ylabel("Average Cluster Variance")
    plt.title("Cluster Variance")
    #plt.legend()
    plt.show()

def plotSilhouetteDetailed(clusterValueDict, trainingExamples):
    for clusterNumber in clusterValueDict:
        fig, ax = plt.subplots()
        fig.set_size_inches(18, 7)
        ax.set_xlim([-0.1, 1])
        ax.set_ylim([0, len(trainingExamples) + (int(clusterNumber) + 1) * 10])
        centroids, varianceList, clusterAssignments_dict, loss = clusterValueDict[clusterNumber]
        clusterAssignments = np.zeros(SIZE)
        for i in clusterAssignments_dict:
            clusterAssignments[int(i)] = clusterAssignments_dict[i]
        silhouette_avg = silhouette_score(trainingExamples, clusterAssignments)
        print(silhouette_avg)
        sample_silhouette_values = silhouette_samples(trainingExamples, clusterAssignments)
        y_lower = 10
        for i in range(int(clusterNumber)):
            ith_cluster_silhouette_values = sample_silhouette_values[clusterAssignments == i]
            ith_cluster_silhouette_values.sort()
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.spectral(float(i) / int(clusterNumber))
            ax.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax.set_title("The silhouette plot for the various clusters.")
        ax.set_xlabel("The silhouette coefficient values")
        ax.set_ylabel("Cluster label")
        # The vertical line for average silhouette score of all the values
        ax.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax.set_yticks([])  # Clear the yaxis labels / ticks
        ax.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        # Labeling the clusters
        plt.suptitle(("Silhouette analysis = %d" % int(clusterNumber)),
                     fontsize=14, fontweight='bold')
        plt.show()

plotOptimalKGraphElbow(clusterValueDict)
plotSilhouette(clusterValueDict, trainingExamples)
plotClusterVariance(clusterValueDict, trainingExamples)
#plotSilhouetteDetailed(clusterValueDict, trainingExamples)
#plotBiasVariance(trainingLossDict, testLossDict)
