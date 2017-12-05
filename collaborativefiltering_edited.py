import json
import random
import math

#reviews = []
mean_rating = 0
businessesToCustomers = {}
customersToBusinesses = {}
count = 0

businessData = []
with open('IL.json', 'r') as f:
	count_2 = 0
	for line in f:
		businessData.append(json.loads(line))
		count_2 += 1
    	#if count_2 == 500: break

businessIDList_training = []
#businessIDList_test = []
for row in businessData:
#    number = random.random()
#    if number > 0.8:
    businessIDList_training.append(row['business_id'])
#    else:
#        businessIDList_test.append(row['business_id'])

print 'Business Done'

with open('review_training.json', 'r') as f:
    for line in f:
        data = json.loads(line)
        count += 1
        if count%10000 == 0:
            print 'Done', count
        if data['business_id'] in businessIDList_training:
        #reviews.append(data)
            mean_rating += data['stars']
            if data['business_id'] in businessesToCustomers:
        		if data['user_id'] not in businessesToCustomers[data['business_id']]:
        			businessesToCustomers[data['business_id']][data['user_id']] = data['stars']
            else:
				businessesToCustomers[data['business_id']] = {}
				businessesToCustomers[data['business_id']][data['user_id']] = data['stars']
            if data['user_id'] in customersToBusinesses:
        		if data['business_id'] not in customersToBusinesses[data['user_id']]:
					customersToBusinesses[data['user_id']][data['business_id']] = data['stars']
            else:
                customersToBusinesses[data['user_id']] = {}
                customersToBusinesses[data['user_id']][data['business_id']] = data['stars']
mean_rating = mean_rating / float(count)

business_ratings = {}
customer_ratings = {}
business_regularization_constant = 0
customer_regularization_constant = 0

for business_id in businessesToCustomers:
    customerBase = businessesToCustomers[business_id]
    business_rating = 0
    for user_id in customerBase:
        rating = customerBase[user_id]
        business_rating += rating # changed from rating - mean_rating
    business_rating = business_rating/float(len(customerBase) + business_regularization_constant)
    business_ratings[business_id] = business_rating
print(business_ratings)

for user_id in customersToBusinesses:
    businessesFrequented = customersToBusinesses[user_id]
    customer_rating = 0
    for business_id in businessesFrequented:
        rating = businessesFrequented[business_id]
        customer_rating += rating #changed from rating - mean_rating - business_ratings[business_id]
    customer_rating = customer_rating/float(len(businessesFrequented) + customer_regularization_constant)
    customer_ratings[user_id] = customer_rating
print(customer_ratings)


similarityDict = {}

#calculate Pearson correlation
for business_id_A in businessesToCustomers:
    for business_id_B in businessesToCustomers:
        if business_id_A != business_id_B:
			numerator = 0
			denominator = 0
			customers_A = businessesToCustomers[business_id_A]
			customers_B = businessesToCustomers[business_id_B]
			for user_id in customers_A:
				if user_id in customers_B:
					#used the similarity measure from milestone - edit if that isn't accurate here
					numerator += (customers_A[user_id] - business_ratings[business_id_A]) * (customers_B[user_id] - business_ratings[business_id_B])
					denominator += ((customers_A[user_id] - business_ratings[business_id_A]) ** 2) * ((customers_B[user_id] - business_ratings[business_id_B]) ** 2)
			similarityDict[business_id_A] = {}
			similarityDict[business_id_B] = {}
			if numerator == 0:
				similarityDict[business_id_A][business_id_B] = 0
				similarityDict[business_id_B][business_id_A] = 0
			else:
				similarityDict[business_id_A][business_id_B] = numerator/float(math.sqrt(denominator))
				similarityDict[business_id_B][business_id_A] = numerator/float(math.sqrt(denominator))

#similarly used prediction formula from milestone
#assumes business_id is mentioned in reviews.json
def prediction(business_id, user_id, similarityDict, businessesToCustomers, business_ratings):
	relevantBusinesses = similarityDict[business_id]
	numerator = 0
	denominator = 0
	for business_id_2 in relevantBusinesses:
		customerBase = businessesToCustomers[business_id_2]
		if user_id in customerBase:
			numerator += (businessesToCustomers[business_id_2][user_id] - business_ratings[business_id_2]) * similarityDict[business_id][business_id_2]
			denominator += similarityDict[business_id][business_id_2]
	if denominator == 0:
		prediction = business_ratings[business_id]
	else:
		prediction = business_ratings[business_id] + (numerator/float(denominator))
	return prediction

## final testing below
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
with open('review_test.json', 'r') as f:
    for line in f:
		predicted_rating = 0
		data = json.loads(line)
		user_id = data['user_id']
		business_id = data['business_id']
		if business_id in businessIDList_training:
			if business_id in business_ratings:
				if user_id in customer_ratings:
					predicted_rating = prediction(business_id, user_id, similarityDict, businessesToCustomers, business_ratings)
					predicted_rating = int(round(predicted_rating))
					if predicted_rating > 5:
						predicted_rating = 5
					if predicted_rating < 1:
						predicted_rating = 1
						print predicted_rating, data['stars']
					if predicted_rating == data['stars']:
						finalscores[0] += 1
					else:
						finalscores[1] += 1
accuracy = finalscores[0]/float(sum(finalscores))
print(accuracy)
