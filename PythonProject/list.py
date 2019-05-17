arr1=[1,2,3]
arr2=[10,"Hello",8.7]
arr1[0]=[1,2,3]

print(type(arr1))
print(arr1)
print(arr2)
print([0]*10)
print(",".join(["walt","is","good"]))
print(list(arr1))

names=["walt","nana","nami"]
passwords=[9,999,9999]
print("names: ",names)
print("passwords: ",passwords)
print("{name : password for name,password in zip(names,passwords)}: ")
print({name : password for name,password in zip(names,passwords)})

