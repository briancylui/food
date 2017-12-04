import json
import random

#reviews = []
mean_rating = 0
businessesToCustomers = {}
customersToBusinesses = {}
count = 0

businessData = []
with open('HLD.json', 'r') as f:
	count_2 = 0
	for line in f:
		businessData.append(json.loads(line))
		count_2 += 1
    	#if count_2 == 10: break

businessIDList_training = []
businessIDList_test = []
for row in businessData:
    number = random.random()
    if number > 0.8:
        businessIDList_training.append(row['business_id'])
    else:
        businessIDList_test.append(row['business_id'])

print 'Business Done'

with open('review_training.json', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data['business_id'] in businessIDList_training:
        #reviews.append(data)
            count += 1
            if count%10000 == 0:
                print 'Done', count
            mean_rating += data['stars']
            if data['business_id'] in businessesToCustomers:
        		if data['user_id'] not in businessesToCustomers[data['business_id']]:
        			businessesToCustomers[data['business_id']].append((data['user_id'], data['stars']))
            else:
                businessesToCustomers[data['business_id']] = [(data['user_id'], data['stars'])]
            if data['user_id'] in customersToBusinesses:
        		if data['business_id'] not in customersToBusinesses[data['user_id']]:
        			customersToBusinesses[data['user_id']].append((data['business_id'], data['stars']))
            else:
                customersToBusinesses[data['user_id']] = [(data['business_id'], data['stars'])]
mean_rating = mean_rating / float(count)

business_ratings = {}
customer_ratings = {}
business_regularization_constant = 0
customer_regularization_constant = 0

for business_id in businessesToCustomers:
    customerBase = businessesToCustomers[business_id]
    business_rating = 0
    for cr in customerBase:
        user_id, rating = cr
        business_rating += (rating - mean_rating) # changed from rating - mean_rating
    business_rating = business_rating/float(len(customerBase) + business_regularization_constant)
    business_ratings[business_id] = business_rating
print(business_ratings)

for user_id in customersToBusinesses:
    businessesFrequented = customersToBusinesses[user_id]
    customer_rating = 0
    for business in businessesFrequented:
        business_id, rating = business
        customer_rating += (rating - mean_rating - business_ratings[business_id]) #changed from rating - mean_rating - business_ratings[business_id]
    customer_rating = customer_rating/float(len(businessesFrequented) + customer_regularization_constant)
    customer_ratings[user_id] = customer_rating
print(customer_ratings)

"""
similarityDict = {}

#calculate Pearson correlation
for business_id_A in businessesToCustomers:
    for business_id_B in businessesToCustomers:
        if business_id_A != business_id_B:
            similarity = 0
            customers_A = businessesToCustomers[business_id_A]
            customers_B = businessesToCustomers[business_id_B]
            for customer_A in customers_A:
                user_id, rating = customer_A

## final testing below
"""
"""
#actual testing
finalscores = [0, 0] #accurate, notaccurate
with open('review_test.json', 'r') as f:
    for line in f:
        data = json.loads(line)
        predicted_rating = mean_rating
        business_id = data['business_id']
        user_id = data['user_id']
        if business_id in business_ratings:
            predicted_rating += business_ratings[business_id]
        if user_id in customer_ratings:
            predicted_rating += customer_ratings[user_id]
        predicted_rating = round(predicted_rating)
        if predicted_rating == data['stars']:
            finalscores[0] += 1
        else:
            finalscores[1] += 1
accuracy = finalscores[0]/float(sum(finalscores))
print(accuracy)
"""

#HLD Testing
finalscores = [0, 0] #accurate, notaccurate
with open('review_training.json', 'r') as f:
    for line in f:
        data = json.loads(line)
        predicted_rating = mean_rating
        business_id = data['business_id']
        user_id = data['user_id']
        if business_id in businessIDList_test:
            if business_id in business_ratings:
                predicted_rating += business_ratings[business_id]
            if user_id in customer_ratings:
                predicted_rating += customer_ratings[user_id]
            predicted_rating = round(predicted_rating)
            if predicted_rating == data['stars']:
                finalscores[0] += 1
            else:
                finalscores[1] += 1
accuracy = finalscores[0]/float(sum(finalscores))
print(accuracy)
