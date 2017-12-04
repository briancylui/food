import json
from random import shuffle

with open('review.json', 'r') as f:
    with open('review_test.json', 'w') as g:
        with open('review_training.json', 'w') as h:
            for line in f:
                data = json.loads(line)
                num = random.random()
                if num > 0.8:
                    json.dump(data, g)
        			f.write('\n')
                else:
                    json.dump(data, h)
        			f.write('\n')


"""
reviews = []
with open('review.json', 'r') as f:
    for line in f:
		reviews.append(json.loads(line))
shuffle(reviews)
test_Number = len(reviews)/5

with open('review_test.json', 'w') as f:
    for i in range(test_Number):
        f.write(reviews[i])
"""
"""
ratingCount = [0,0,0,0,0,0]
with open('review.json', 'r') as f:
	for line in f:
		jsonLine = json.loads(line)
		ratingCount[jsonLine['stars']] += 1

print ratingCount

mean_rating = 0
for i in range(ratingCount):
    mean_rating += i * ratingCount[i]

mean_rating = mean_rating/float(sum(ratingCount))

print(mean_rating)
"""
