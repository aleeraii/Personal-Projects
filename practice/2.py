f = open('data/test', 'r')
data = f.read().split('-')
data.pop(0)
for v in data:
    li1 = v.split('\n')
print(li1)