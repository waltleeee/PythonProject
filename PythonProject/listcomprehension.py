import time

arr1=[]

for i in range(10):
    arr1.append(i)
print(arr1)    

arr2=[i for i in range(10)]
print(arr2)

arr3=[i for i in arr2 if i%2==0]
print(arr3)

arr4=[i for i in arr2 if i>=3 and i%2]
print(arr4)

arr5=[(x,y) for x in range(3) for y in range(4)]
print(arr5)

arr6 = []
s = time.time()
for i in range(int(1e+6)):
    arr6.append(i)
print('took {} secs'.format(round(time.time() - s, 3)))

s = time.time()
arr7 = [i for i in range(int(1e+6))]
print('took {} secs'.format(round(time.time() - s, 3)))

comp = (i for i in range(10))
print(comp)
print(type(comp))

arr8 = list(comp)
arr9 = list(comp)
arr10 = [comp]
print(arr8)
print(arr9)
print(arr10)

arr11=[1,3,5,7,9,11,13,15,17,19]
arr12=[2,4,6,8,10,12,14,16,18,20]

for i in range(len(arr11)):
    print(arr11[i],"<--->",arr12[i])
    