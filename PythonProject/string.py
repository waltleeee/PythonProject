import sys

str1="hello pythin"
str2=str1
str2+=" JJJ"
print(str2 is str1)#check same memory position or not

print(str1)
result=str2.split(" ")
print(result)
result_back="***".join(str1)
print(result_back)
result_back2="***".join(result)
print(result_back2)

print("c:\todo")
print("c:\\todo")

print(r"c:\todo")
print(r"c:\\todo")    

name="walt"
print("name: ",name)
print("walt" in name)
print("walts" in name)
print("name+name: ",name+name)
print("name*3: ",name*3)    
print("name[0]: ",name[0])
print("name[2]: ",name[2])
print("name[1:3]: ",name[1:3])
print("name[0:4:2]: ",name[0:4:2])
print("name[::-1]: ",name[::-1])
print("name[0:]: ",name[0:])
print("name[:2]: ",name[:2])
print("name[-1]: ",name[-1])
print("name[-2]: ",name[-2])

print("{0} is {1}".format("walt","good"))
print("{a} is {b}".format(a="walt",b="man"))
print("{0} is {c}".format("walt",c="m"))
print("MY PLATFORM is {pc.platform}".format(pc=sys))
