import json

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

userList = ['kzyLOqiJvyw_FWFTw2rjiQ','WZXp9-V2dqRRJqhGgRqueA','XylT12exfdLiI_3uDLVIpw','Ji9PeffxjwqPLO7pEfSpKQ','TLIWzAJPrET0zX4_vgvLhg','PY_VIzS-joaY2me4K4HyPQ','5QBtIy-aUrg9BdsxqhqORA','n6VF7X8cSEN3UjR2n21Rqw','cSGIyH2RV8QU_hC4aDPPfA','Z9K80hzxdvT3T4QX4tAUOw']

relevantReview = []
with open('review.json', 'r') as f:
	for line in f:
		jsonLine = json.loads(line)
		if jsonLine['business_id'] in businessIDList and jsonLine['user_id'] in userList:
			relevantReview.append(jsonLine)

for review in relevantReview:
	print 'Business:', review['business_id'], 'User:', review['user_id'], 'Star-rating:', review['stars']