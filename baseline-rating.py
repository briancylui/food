import json

ratingCount = [0,0,0,0,0,0]
with open('review.json', 'r') as f:
	for line in f:
		jsonLine = json.loads(line)
		ratingCount[jsonLine['stars']] += 1

print ratingCount