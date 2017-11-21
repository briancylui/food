import json
import csv
#from pprint import pprint
#business = open('business.json','r').read()
#user = open('user.json','r')
#review = open('review.json')
#checkin = open('checkin.json')

businessData = []
with open('business.json', 'r') as f:
	count = 0
	for line in f:
		businessData.append(json.loads(line))
		count += 1
    	#if count == 10: break

businessIDList = []
for row in businessData:
    businessIDList.append(row['business_id'])

print 'Business Done'

#categoriesToRestaurants = {}
#for data in businessData:
#	ctgList = data['categories']
#	for ctg in ctgList:
#		if ctg in categoriesToRestaurants:
#			categoriesToRestaurants[ctg].append(data['business_id'])
#		else:
#			categoriesToRestaurants[ctg] = [data['business_id']]
#print categoriesToRestaurants

relevantReview = []
with open('review.json', 'r') as f:
	for line in f:
		jsonLine = json.loads(line)
		if jsonLine['business_id'] in businessIDList:
			relevantReview.append(jsonLine)

relevantTip = []
with open('tip.json', 'r') as f:
	for line in f:
		jsonLine = json.loads(line)
		if jsonLine['business_id'] in businessIDList:
			relevantTip.append(jsonLine)

restToUser = {}
for review in relevantReview:
	if review['business_id'] in restToUser:
		if review['user_id'] not in restToUser[review['business_id']]:
			restToUser[review['business_id']].append(review['user_id'])
	else:
		restToUser[review['business_id']] = [review['user_id']]

print 'Review Done'

for review in relevantTip:
	if review['business_id'] in restToUser:
		if review['user_id'] not in restToUser[review['business_id']]:
			restToUser[review['business_id']].append(review['user_id'])
	else:
		restToUser[review['business_id']] = [review['user_id']]

print 'Tip Done'

with open('common-user.csv', 'w') as csvfile:
	wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for rest in restToUser:
		wrt.writerow([rest] + restToUser[rest])
