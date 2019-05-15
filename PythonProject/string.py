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