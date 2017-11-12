import json
#from pprint import pprint
#business = open('business.json','r').read()
#user = open('user.json','r')
#review = open('review.json')
#checkin = open('checkin.json')

businessData = []
with open('businessSmall.json', 'r') as f:
	count = 0
	for line in f:
		businessData.append(json.loads(line))
		count += 1
    	#if count == 10: break

businessIDList = []
for row in businessData:
    businessIDList.append(row['business_id'])

categoriesToRestaurants = {}
for data in businessData:
	ctgList = data['categories']
	for ctg in ctgList:
		if ctg in categoriesToRestaurants:
			categoriesToRestaurants[ctg].append(data['business_id'])
		else:
			categoriesToRestaurants[ctg] = [data['business_id']]
#print categoriesToRestaurants

relevantReview = []
with open('review.json', 'r') as f:
	for line in f:
		jsonLine = json.loads(line)
		if jsonLine['business_id'] in businessIDList:
			relevantReview.append(jsonLine)

#relevantUser = []
#for review in relevantReview:
#	relevantUser.append(review['user_id'])

categoriesToUsers = {}
for ctg in categoriesToRestaurants:
	restList = categoriesToRestaurants[ctg]
	for review in relevantReview:
		if review['business_id'] in restList:
			if ctg in categoriesToUsers:
				categoriesToUsers[ctg].append(review['user_id'])
			else:
				categoriesToUsers[ctg] = [review['user_id']]

for data in businessData:
	ctgList = data['categories']
	finalUserList = []
	for ctg in ctgList:
		finalUserList += categoriesToUsers[ctg]
	print 'For business with business_id:', data['business_id'], 'the suggested list of users is', finalUserList

#print businessIDList


#print relevantReview
#businessData = []
#for line in business:
#	businessData.append(json.loads(line))
#userData = json.loads(user)
#reviewData = json.loads(review)
#checkInData = json.loads(checkin)

#pprint(businessData)