import json

businessData = []
with open('business.json', 'r') as f:
	count = 0
	for line in f:
		businessData.append(json.loads(line))
		count += 1
    	#if count == 10: break

count = 0
with open('HLD.json', 'w') as f:
	for data in businessData:
		if data['state'] == 'HLD':
			json.dump(data, f)
			f.write('\n')
		count += 1
		if count%1000 == 0:
			print count

