import json as js
import numpy as np
import math
from collections import defaultdict
import csv
import pickle
import os.path

# Open the business JSON file.
businesses = []
with open('dataset/business.json', 'r') as business_file:
    print 'Opened business.json file.'
    for line in business_file:
        businesses.append(js.loads(line))
    print 'Finished loading business.json.'

# desired output: dict[K] = tuple([all centroids], dict(cluster assignment), y (elbow loss)) for cross validation of K

# Functions
def optimal_K():
    return 10

def optimal_alpha():
    return 0.1

def optimal_beta():
    return 0.1

# Hyper-parameters
K_opt = optimal_K()
alpha = optimal_alpha()
beta = optimal_beta()
num_iter = 100
convergence_threshold = 1e-3

# Constants
N = len(businesses)

# Import Richard's csv files
related = defaultdict(float)
business_types = defaultdict(string)
if os.path.isfile('relatedness.pkl'):
    with open('relatedness.pkl', 'rb') as f:
        related = pickle.load(f)
else:
    cat_proportion = csv.reader(open('cat-proportion-shortened.csv'))
    related_cats = defaultdict(float)
    for line in cat_proportion:
        related_cats[(line[0], line[1])] = float(line[2])
    for key, value in related_cats.items():
        cat1, cat2 = key
        if cat1 not in business_types:
            business_types.append(cat1)
        if cat2 not in business_types:
            business_types.append(cat2)
        i = business_types.index(cat1)
        j = business_types.index(cat2)
        if (i, j) not in related:
            related[(i, j)] = value
        if (j, i) not in related:
            related[(j, i)] = value

    with open('relatedness.pkl', 'wb') as f:
        pickle.dump(related, f, pickle.HIGHEST_PROTOCOL)
    with 

'''
# Relatedness function for business types
print 'Start constructing relatedness table.'
related = defaultdict(float)
for i in range(N):
    for j in range(i, N):
        print '%d %d' % (i, j)
        num_common_types = len({c for c in businesses[i]['categories'] if c in businesses[j]['categories']})
        if num_common_types == 0:
            related[(i, j)] = 0
            related[(j, i)] = 0
            continue

        denominator = len(businesses[i]['categories']) + len(businesses[j]['categories']) - num_common_types
        print num_common_types, denominator
        related[(i, j)] = num_common_types * 1. / denominator if denominator != 0 else 0
        related[(j, i)] = related[(i, j)]
'''

# Distance function for K-means clustering
dist = defaultdict(float) # distance of (i, j)
print 'Find stored distance function.'
if os.path.isfile('distance.pkl'):
    print 'Retrieve previous distance function'
    with open('distance.pkl', 'rb') as f:
        dist = pickle.load(f)
    print 'Finished loading distance function'
else:
    print 'Start constructing distance table.'
    for i in range(N):
        for j in range(i, N):
            dist[(i, j)] = math.sqrt((businesses[i]['stars'] - businesses[j]['stars']) ** 2 + (businesses[i]['review_count'] - businesses[j]['review_count']) ** 2) + alpha * sum(1 - max(related[(x, y)] for y in businesses[j]['categories']) for x in businesses[i]['categories'])
            if i != j: dist[(j, i)] = dist[(i, j)]
    print 'Finished constructing distance table.'
    with open('distance.pkl', 'wb') as f:
        pickle.dump(dist, f, pickle.HIGHEST_PROTOCOL)
    print 'Saved new distance function'


def clustering(K, num_iter, convergence_threshold, N):
    print 'Start %d-means clustering' % K

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
for i in range(2 * K_opt):
    cross_validate_K[i] = clustering(i, num_iter, convergence_threshold, N)

with open('cvK.json', 'w') as cvKfile:
    json.dump(cross_validate_K,cvKfile)

# Joel: The dictionary you want is exactly cross_validate_K here.  Get this dict from the cvK.json file by typing:
# with open('cvK.json', 'r') as readcvK:
#     cross_validate_K = js.load(readcvK)


