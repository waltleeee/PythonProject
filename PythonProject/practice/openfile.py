import sys
print("OPEN START")
# fileWrite=open(sys.argv[0],"w")
# fileWrite.write("test")
# fileWrite.close()

# file=open(sys.argv[0],"r")
# content=file.read()
# file.close()
# print(content)

for line in open(sys.argv[0],"r"):
    print(line,end="")