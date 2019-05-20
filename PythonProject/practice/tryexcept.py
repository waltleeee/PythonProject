import sys

try:
    file= open(sys.argv[1],"r")
    try:
        for line in file:
            print(line,end=" ")
    finally:#must do
        if file:
            file.close()
except IndexError:
    print("INDEX ERROR")
   
#RAISE TEST,will return error      
# print("!!!!!!!!RAISE TEST")
# try:
#     file= open(sys.argv[1],"r")
#     try:
#         for line in file:
#             print(line,end=" ")
#     finally:#must do
#         if file:
#             file.close()
# except IndexError:
#     print("INDEX ERROR")
#     raise

print("!!!!!!!!ERROR VAR TEST")
try:
    file= open(sys.argv[1],"r")
    try:
        for line in file:
            print(line,end=" ")
    finally:#must do
        if file:
            file.close()
except IndexError as e:
    print(type(e),str(e))
    raise e