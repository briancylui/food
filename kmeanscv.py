import json as js
import numpy as np
import math
from collections import defaultdict
import csv
import pickle
import os.path
import random
import matplotlib.pyplot as plt
import sklearn.model_selection as skl

# Open the business JSON file.
state = 'HLD'
businesses = []
with open(state + '.json', 'r') as business_file:
    print 'Opened business.json file.'
    for line in business_file:
        businesses.append(js.loads(line))
    print 'Finished loading business.json.'

# desired output: dict[K] = tuple([all centroids], dict(cluster assignment), y (elbow loss)) for cross validation of K

# Functions
def optimal_K():
    return 10

def optimal_alpha():
    return 0.6

def optimal_beta():
    return 0.1

# Hyper-parameters
K_opt = optimal_K()
alpha = optimal_alpha()
beta = optimal_beta()
num_iter = 100
convergence_threshold = 3

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
        pickle.dump(business_types, f, pickle.HIGHESTt_PROTOCOL)
print("Done! - First step")

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
similarity = defaultdict(float)
print 'Find stored distance function.'
if os.path.isfile('distance' + state + '.pkl'):
    print 'Retrieve previous distance function'
    with open('distance' + state + '.pkl', 'rb') as f:
        dist = pickle.load(f)
    print 'Finished loading distance function'
else:

    # Squared difference of ratings
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

    # Squared difference of review counts
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

    # Relatedness difference
    if os.path.isfile('related_diff' + state + '.pkl'):
        with open('related_diff' + state + '.pkl', 'rb') as f:
            related_diff = pickle.load(f)
    else:
        print 'Start constructing related_diff table'
        for i in range(N):
            for j in range(i, N):
                related_diff[(i, j)] = max([1 - max([related[(business_types.index(x), business_types.index(y))] for y in businesses[j]['categories']] or [0]) for x in businesses[i]['categories']] or [0])
#                print 'related_diff[(%d, %d)] = %.5f' % (i, j, related_diff[(i, j)])
                if i != j: related_diff[(j, i)] = related_diff[(i, j)]
        with open('related_diff' + state + '.pkl', 'wb') as f:
            pickle.dump(related_diff, f,pickle.HIGHEST_PROTOCOL)
        print 'Finished constructing related_diff table'

    # Common user proportion
    if os.path.isfile('common-user-prop-' + state + '.csv'):
        with open('common-user-prop-' + state + '.csv', 'rb') as f:
            reader = csv.reader(f, delimiter = ',', quotechar = '|')
            for row in reader:
                if float(row[2]) == 0:
                    similarity[(row[0], row[1])] = 100000
                    similarity[(row[1], row[0])] = 100000
                else:
                    similarity[(row[0], row[1])] = 1/float(row[2])
                    similarity[(row[1], row[0])] = 1/float(row[2])
    else:
        raise "Where is common user??"
    minimum_review_count = min(sq_diff_review_counts.values())
    maximum_review_count = max(sq_diff_review_counts.values())
    minimum_ratings = min(sq_diff_ratings.values())
    maximum_ratings = max(sq_diff_ratings.values())
    max_similarity = 100000
    min_similarity = min(similarity.values())
    print 'Start constructing distance table.'
    for i in range(N):
        for j in range(i, N):
            dist[(i, j)] = (1 - alpha) * math.sqrt((sq_diff_ratings[(i, j)] - minimum_ratings)/float(maximum_ratings - minimum_ratings) + (sq_diff_review_counts[(i, j)] - minimum_ratings)/float(maximum_ratings - minimum_ratings)) + alpha * (related_diff[(i, j)] + (similarity[(i, j)] - min_similarity)/float(max_similarity - min_similarity))
            #print 'dist[(%d, %d)] = %.2f' % (i, j, dist[(i, j)])
            if i != j: dist[(j, i)] = dist[(i, j)]
    print 'Finished constructing distance table.'
    with open('distance' + state + '.pkl', 'wb') as f:
        pickle.dump(dist, f, pickle.HIGHEST_PROTOCOL)
    print 'Saved new distance function'


def clustering(K, num_iter, convergence_threshold, indices, cross_validate):
    print 'Start %d-means clustering' % K

    centroid_of = defaultdict(int) # assignment of i
    centroid = random.sample(indices, K)
    cluster_var = defaultdict(float)

    consecutive_no_learning_trials = 0
    for iter in range(num_iter):
        if consecutive_no_learning_trials > convergence_threshold: break
        # If average change in centroids is smaller than convergence_threshold, then break.
        num_of_centroid_changes = 0
        # Assignment step:
        for i in indices:
            centroid_of[i] = min((dist[(i, j)], j) for j in centroid)[1]

        if cross_validate:
            cluster_var[i] = min( sum([dist[(j, k)] for k in businesses_in_cluster] ) * 1. / len(businesses_in_cluster) for j in businesses_in_cluster) if businesses_in_cluster else (0, random.choice(indices))
            loss = sum(dist[(i, centroid_of[i])] for i in indices) * 1. / len(indices)
            return (centroid, cluster_var, centroid_of, loss)

        # Adjustment step:
        for i in range(K):
            businesses_in_cluster = [b for b in indices if centroid_of[b] == centroid[i]]
            old_centroid = centroid[i]
            cluster_var[i], centroid[i] = min(( sum([dist[(j, k)] for k in businesses_in_cluster] ) * 1. / len(businesses_in_cluster) , j) for j in businesses_in_cluster) if businesses_in_cluster else (0, random.choice(indices))
            if old_centroid != centroid[i]: num_of_centroid_changes += 1

        # Evaluation
        ratio_of_centroid_changes = num_of_centroid_changes * 1. / K
        if ratio_of_centroid_changes == 0: consecutive_no_learning_trials += 1
        else: consecutive_no_learning_trials == 0
        print 'Iteration %d: centroids:' % iter
        print centroid

        #if ratio_of_centroid_changes < convergence_threshold: break

    loss = sum(dist[(i, centroid_of[i])] for i in indices) * 1. / len(indices)
    return (centroid, cluster_var, centroid_of, loss)

def cross_validate(i, num_iter, convergence_threshold, N, m):
    if m == 0: return clustering(i, num_iter, convergence_threshold, range(N), False)

    kf = skl.KFold(n_splits=m, shuffle=True)
    train_result = {}
    cv_result = {}

    for count in range(m):
        for train_indices, cv_indices in kf.split(range(int(0.9 * N))):
            train_result[count] = clustering(i, num_iter, convergence_threshold, train_indices, False)
            cv_result[count] = clustering(i, num_iter, convergence_threshold, cv_indices, True)
        
    return sum(elem[3] for elem in cv_result) * 1. / len(cv_result)


cross_validate_K = dict()
for i in range(1, 2 * K_opt + 1):
    cross_validate_K[i] = cross_validate(i, num_iter, convergence_threshold, N, m=5)

optimalK = min((cross_validate_K[key], key) for key in cross_validate_K)[1]

test_result = cross_validate(optimalK, num_iter, convergence_threshold, N, m=0)

cluster_num = np.arange(1, 2 * K_opt + 1)
cv_losses = np.array([cross_validate_K[i] for i in cross_validate_K])
plt.plot(cluster_num, cv_losses)
plt.xlabel('Number of clusters')
plt.ylabel('Dev-set loss')
plt.title('5-fold cross validation for the optimal number of clusters')
plt.show()
print test_result[3]

'''
with open('cvK' + state + '.json', 'w') as cvKfile:
    js.dump(cross_validate_K,cvKfile)

losses = np.array([cross_validate_K[i][3] for i in range(1, 2 * K_opt + 1)])
cluster_num = np.arange(1, 2 * K_opt + 1)
plt.plot(cluster_num, losses)
plt.xlabel('Number of clusters')
plt.ylabel('Loss')
plt.show()
'''

# Joel: The dictionary you want is exactly cross_validate_K here.  Get this dict from the cvK.json file by typing:
# with open('cvK.json', 'r') as readcvK:
#     cross_validate_K = js.load(readcvK)
