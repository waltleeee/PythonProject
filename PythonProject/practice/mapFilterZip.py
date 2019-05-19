def filterTest(inFunction,inList):
	result=[]
	for ele in inList:
		if inFunction(ele):
			result.append(ele)
	return result

lt=["abc","aBcd","abcde","abcdef"]
print("TEST A: ",filterTest(lambda ele :len(ele)>4,lt))
print("TEST B: ",filterTest(lambda ele: "B" in ele,lt))

#PYTHON LIB

print(list(filter(lambda ele: len(ele) > 6, lt)))#because filter and map will return generator not list,so need use list to transform
print(list(filter(lambda ele: 'e' in ele,lt)))
print(list(map(lambda ele: ele.upper(), lt)))
print(list(map(lambda ele: len(ele), lt)))


arr13=[i for i in range(1,21,2)]
arr14=[i for i in range(2,21,2)]

for i,j in zip(arr13,arr14):
    print(i,j,sep="<-->")    

print(list(zip(arr13,arr14)))