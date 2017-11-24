import json, csv
from sets import Set

categoryToBID = {}
categoryList = []
with open('cat-bid.csv', 'rb') as csvfile:
	alldata = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in alldata:
		categoryToBID[row[0]] = Set(row[1:])
		categoryList.append(row[0])
#print businessToUser
#print businessList

commonBusiness = {}
allBusiness = {}
proportion ={}
count = 0
for ctg1 in categoryList:
	count += 1
	print count
	for ctg2 in categoryList:
		commonBusiness[(ctg1, ctg2)] = categoryToBID[ctg1] & categoryToBID[ctg2]
		allBusiness[(ctg1, ctg2)] = categoryToBID[ctg1] | categoryToBID[ctg2]
		proportion[(ctg1, ctg2)] = float(len(commonBusiness[(ctg1, ctg2)]))/len(allBusiness[(ctg1, ctg2)])

#with open('cat-intersection.csv', 'w') as csvfile:
#	wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#	for pair in commonBusiness:
#		wrt.writerow([pair[0], pair[1]] + list(commonBusiness[pair]))
#print 'Intersection done'

#with open('cat-union.csv', 'w') as csvfile:
#	wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#	for pair in allBusiness:
#		wrt.writerow([pair[0], pair[1]] + list(allBusiness[pair]))
#print 'Union done'

with open('cat-proportion.csv', 'w') as csvfile:
	wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	for pair in proportion:
		wrt.writerow([pair[0], pair[1], proportion[pair]])
print 'Proportion done'
