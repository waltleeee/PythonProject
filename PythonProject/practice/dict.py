passwords={"walt":123456,"nana":12}
print(passwords["walt"])

passwords["nami"]=456
print(passwords)

del passwords["walt"]
print(passwords)

print("passwords.items()",passwords.items())
print("passwords.keys()",passwords.keys())
print("passwords.values()",passwords.values())
print("passwords.get(123,default value)",passwords.get("XXX","YYY"))