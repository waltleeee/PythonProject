def max(a,b):
    return a if a>b else b

def min(a,b):
    return a if a<b else b

print(max(10,5))

maxf=max
print(maxf(11,6))

minf=lambda a,b:a if a<b else b
print(minf(5,6))
minf2=minf
print(minf2(9,15))