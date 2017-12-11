import json as js
import numpy as np
import math
from collections import defaultdict
import csv
import pickle
import os.path
import random

# Open the business JSON file.
state = 'IL'
businesses = []
with open('dataset/' + state + '.json', 'r') as business_file:
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
business_types = []
if os.path.isfile('relatedness.pkl') and os.path.isfile('businesstypes.pkl'):
    with open('relatedness.pkl', 'rb') as f:
        related = pickle.load(f)
    with open('businesstypes.pkl', 'rb') as f:
        business_types = pickle.load(f)
        
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
    with open('businesstypes.pkl', 'wb') as f:
        pickle.dump(business_types, f, pickle.HIGHEST_PROTOCOL)


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
sq_diff_ratings = defaultdict(int)
sq_diff_review_counts = defaultdict(int)
related_diff = defaultdict(float)
print 'Find stored distance function.'
if os.path.isfile('distance' + state + '.pkl'):
    print 'Retrieve previous distance function'
    with open('distance' + state + '.pkl', 'rb') as f:
        dist = pickle.load(f)
    print 'Finished loading distance function'
else:
    if os.path.isfile('sq_diff_ratings' + state + '.pkl'):
        with open('sq_diff_ratings' + state + '.pkl', 'rb') as f:
            sq_diff_ratings = pickle.load(f)
    else:
        print 'Start constructing sq_diff_ratings table'
        for i in range(N):
            for j in range(i, N):
                sq_diff_ratings[(i, j)] = (businesses[i]['stars'] - businesses[j]['stars']) ** 2
                if i != j: sq_diff_ratings[(j, i)] = sq_diff_ratings[(i, j)]
        with open('sq_diff_ratings' + state + '.pkl', 'wb') as f:
            pickle.dump(sq_diff_ratings, f, pickle.HIGHEST_PROTOCOL)
        print 'Finished constructing sq_diff_ratings table'

    if os.path.isfile('sq_diff_review_counts' + state + '.pkl'):
        with open('sq_diff_review_counts' + state + '.pkl', 'rb') as f:
            sq_diff_review_counts = pickle.load(f)
    else:
        print 'Start constructing sq_diff_review_counts table'
        for i in range(N):
            for j in range(i, N):
                sq_diff_review_counts[(i, j)] = (businesses[i]['review_count'] - businesses[j]['review_count']) ** 2
                if i != j: sq_diff_review_counts[(j, i)] = sq_diff_review_counts[(i, j)]
        with open('sq_diff_review_counts' + state + '.pkl', 'wb') as f:
            pickle.dump(sq_diff_review_counts, f,pickle.HIGHEST_PROTOCOL)
        print 'Finished constructing sq_diff_review_counts table'

    if os.path.isfile('related_diff' + state + '.pkl'):
        with open('related_diff' + state + '.pkl', 'rb') as f:
            related_diff = pickle.load(f)
    else:
        print 'Start constructing related_diff table'
        for i in range(N):
            for j in range(i, N):
                related_diff[(i, j)] = sum(1 - max([related[(business_types.index(x), business_types.index(y))] for y in businesses[j]['categories']] or [0]) for x in businesses[i]['categories'])
#                print 'related_diff[(%d, %d)] = %.5f' % (i, j, related_diff[(i, j)])
                if i != j: related_diff[(j, i)] = related_diff[(i, j)]
        with open('related_diff' + state + '.pkl', 'wb') as f:
            pickle.dump(related_diff, f,pickle.HIGHEST_PROTOCOL)
        print 'Finished constructing related_diff table'

    print 'Start constructing distance table.'
    for i in range(N):
        for j in range(i, N):
            dist[(i, j)] = math.sqrt(sq_diff_ratings[(i, j)] + sq_diff_review_counts[(i, j)]) + alpha * related_diff[(i, j)]
            #print 'dist[(%d, %d)] = %.2f' % (i, j, dist[(i, j)])
            if i != j: dist[(j, i)] = dist[(i, j)]
    print 'Finished constructing distance table.'
    with open('distance' + state + '.pkl', 'wb') as f:
        pickle.dump(dist, f, pickle.HIGHEST_PROTOCOL)
    print 'Saved new distance function'


def clustering(K, num_iter, convergence_threshold, N):
    print 'Start %d-means clustering' % K

    centroid_of = defaultdict(int) # assignment of i
    centroid = random.sample(range(N), K)
    cluster_var = defaultdict(float)


    for iter in range(num_iter):
        # If average change in centroids is smaller than convergence_threshold, then break.
        num_of_centroid_changes = 0
        # Assignment step:
        for i in range(N):
            centroid_of[i] = min((dist[(i, j)], j) for j in centroid)[1]

            #num_of_centroid_changes = 0
        # Adjustment step:
        for i in range(len(centroid)):
            businesses_in_cluster = [b for b in range(N) if centroid_of[b] == i]
            old_centroid = centroid[i]
            cluster_var[i], centroid[i] = min(( sum(dist[(j, k)] for k in businesses_in_cluster) * 1. / len(businesses_in_cluster) , j) for j in businesses_in_cluster)
            if old_centroid != centroid[i]: num_of_centroid_changes += 1

        # Evaluation
        ratio_of_centroid_changes = num_of_centroid_changes * 1. / K
        print 'Iteration %d: centroids:' % iter
        print centroid

        #if ratio_of_centroid_changes < convergence_threshold: break
    
    loss = sum(dist[(i, centroid_of[i])] for i in range(N)) * 1. / N
    return (centroid, cluster_var, centroid_of, loss)
    
cross_validate_K = dict()
for i in range(1, 2 * K_opt):
    cross_validate_K[i] = clustering(i, num_iter, convergence_threshold, N)

with open('cvK' + state + '.json', 'w') as cvKfile:
    js.dump(cross_validate_K,cvKfile)

# Joel: The dictionary you want is exactly cross_validate_K here.  Get this dict from the cvK.json file by typing:
# with open('cvK.json', 'r') as readcvK:
#     cross_validate_K = js.load(readcvK)


