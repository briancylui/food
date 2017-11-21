import json
import csv

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

categoriesToRestaurants = {}
for data in businessData:
	ctgList = data['categories']
	for ctg in ctgList:
		if ctg in categoriesToRestaurants:
			categoriesToRestaurants[ctg].append(data['business_id'])
		else:
			categoriesToRestaurants[ctg] = [data['business_id']]
#print categoriesToRestaurants

with open('cat-bid.csv', 'w') as csvfile:
	wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for ctg in categoriesToRestaurants:
		wrt.writerow([ctg] + categoriesToRestaurants[ctg])

