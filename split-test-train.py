import json
import random
from random import shuffle

count = 0
with open('review.json', 'r') as f:
    with open('review_test.json', 'w') as g:
        with open('review_training.json', 'w') as h:
            for line in f:
            	count += 1
            	if count%10000 == 0:
            		print 'Done', count, 'out of 4736897'
                data = json.loads(line)
                num = random.random()
                if num > 0.8:
                    json.dump(data, g)
                    g.write('\n')
                else:
                    json.dump(data, h)
                    h.write('\n')

