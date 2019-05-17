print("ENTER TWO NUMBER...")
m=int(input("Number 1: "))
n=int(input("Number 2: "))
while n!=0:
    r=m%n
    m=n
    n=r
print("GCD: {0}".format(m))     
