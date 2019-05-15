str1="hello pythin"
arr1=[1,2,3,4,5,6,7,8,9]
arr2=arr1[0:5]
arr3=arr1[0:-1:2]#start:stop:step , -1 is maen last element,stop element will not be get
arr4=arr1[:]

print(arr1)
print(arr2)
print(arr3)
print(arr4)
print(arr4 is arr1)
print(str1[5:])
print(arr1[:-1])

print("OTHER CONTROL")

arr5=[1,2,3]
arr6=[4,5]
t=4
print("arr5: [1,2,3]")
print("arr6: [4,5]")
print("t: 4")

print("t in arr5: ",t in arr5)
print("t in arr6: ",t in arr6)
print("t not in arr5",t not in arr5)
print("t not in arr6",t not in arr6)
arr7=arr5+arr6
arr8=arr6*3
print("arr7=arr5+arr6: ",arr7)
print("arr8=arr6*3: ",arr8)
print("len(arr6): ",len(arr6))
print("min(arr6): ",min(arr6))
print("max(arr6): ",max(arr6))
print("arr7.index(3,0,3): ",arr7.index(3,0,3))#value startIndex stopIndex,find value index
print("arr8.count(4): ",arr8.count(4))#find value count

arr8[0]=1
print("arr8[0]=1   arr8: ",arr8)
arr8[2:3]=[9,9]
print("arr8[2:3]=[9,9]  arr8: ",arr8)
arr8[2:4:1]=[2,2,2]
print("arr8[2:4:1]=[2,2,2]  arr8: ",arr8)
del arr8[4:5]
print("del arr8[4:5] arr8: ",arr8)
del arr8[2:3:1]
print("del arr8[2:3:1] arr8:",arr8)
arr8.append(9)
print("arr8.append(9) arr8:",arr8)
arr9=arr8.copy()
print("arr9=arr8.copy() arr9:",arr9)
arr8.clear()
print("arr8.clear() arr8:",arr8)
arr8.extend([5,6,5,6])
print("arr8.extend([5,6,5,6]) arr8:",arr8)
arr8.insert(1,99)
print("arr8.insert(1,99) arr8:",arr8)
x=arr8.pop(0)
print("x=arr8.pop([0]) x:",x," arr8:",arr8)
arr8.remove(6)
print("arr8.remove(6) arr8:",arr8)
arr8.reverse()
print("arr8.reverse() arr8:",arr8)