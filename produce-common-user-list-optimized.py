import json, csv
from sets import Set

businessToUser = {}
businessList = []
with open('common-user-NC.csv', 'rb') as csvfile:
	alldata = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in alldata:
		businessToUser[row[0]] = Set(row[1:])
		businessList.append(row[0])

with open('common-user-prop-NC.csv', 'w') as csvfile:
	wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	count = 0
	for business1 in businessList:
		count += 1
		if count%25 == 0: 
			print count
		for business2 in businessList:
			commonUser = businessToUser[business1] & businessToUser[business2]
			allUser= businessToUser[business1] | businessToUser[business2]
			proportion = float(len(commonUser))/len(allUser)
			if proportion > 0:
				wrt.writerow([business1, business2, proportion])
print 'Proportion done'