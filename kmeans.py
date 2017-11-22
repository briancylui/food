import json as js
import numpy as np
import math

# Open the business JSON file.
businesses = []
with open('dataset/business.json', 'r') as business_file:
    for line in business_file:
        businesses.append(js.loads(line))

# desired output: dict[K] = tuple([all centroids], dict(cluster assignment), y (elbow loss)) for cross validation of K

# Functions
def optimal_K():
    return 10

def optimal_alpha():
    return 0.1

def optimal_beta():
    return 0.1

# Hyper-parameters
K = optimal_K():
alpha = optimal_alpha()
beta = optimal_beta()
num_iter = 100
convergence_threshold = 1e-3

# Relatedness function for the distance function
related = defaultdict(float)
for i in range(N):
    for j in range(i, N):
        num_common_types = len(c for c in businesses[i]['categories'] if c in businesses[j]['categories'])
        related[(i, j)] = num_common_types * 1. / (len(businesses[i]['categories']) + len(businesses[j]['categories']) - num_common_types)
        related[(j, i)] = related[(i, j)]

# Distance function for K-means clustering
dist = defaultdict(float) # distance of (i, j)
N = len(businesses)
for i in range(N):
    for j in range(i, N):
        dist[(i, j)] = math.sqrt((businesses[i]['stars'] - businesses[j]['stars']) ** 2 + (businesses[i]['review_count'] - businesses[j]['review_count']) ** 2) + alpha * sum(1 - max(related[(x, y)] for y in businesses[j]['categories']) for x in businesses[i]['categories'])
        dist[(j, i)] = dist[(i, j)]

def clustering(K, num_iter, convergence_threshold, N):
    centroid_of = defaultdict(int) # assignment of i
    centroid = [0] * K
    cluster_var = defaultdict(float)

    for iter in range(num_iter):
        # If average change in centroids is smaller than convergence_threshold, then break.
        
        # Assignment step:
        for i in range(N):
            centroid_of[i] = min((dist[(i, j)], j) for j in range(K))[1]
            
            num_of_centroid_changes = 0
        # Adjustment step:
        for i in range(K):
            businesses_in_cluster = [b for b in range(N) if centroid_of[b] == i]
            old_centroid = centroid[i]
            cluster_var[i], centroid[i] = min(( sum(dist[(j, k)] for k in businesses_in_cluster) * 1. / len(businesses_in_cluster) , j) for j in businesses_in_cluster)
            if old_centroid != centroid[i]: num_of_centroid_changes += 1

        # Evaluation
        ratio_of_centroid_changes = num_of_centroid_changes * 1. / K
        print 'Iteration %d: centroids:' % iter
        print centroid

        if ratio_of_centroid_changes < convergence_threshold: break
    
    loss = sum(dist[(i, centroid_of[i])] for i in range(N)) * 1. / N
    return (centroid, cluster_var, centroid_of, loss)
    
cross_validate_K = dict()
for i in range(K):
    cross_validate_K[i] = clustering(i, num_iter, convergence_threshold, N)

# Joel: The dictionary you want is exactly cross_validate_K here.
