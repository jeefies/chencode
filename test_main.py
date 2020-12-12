from main import easy_chchr as chchr
from main import encode, easy_chord

lts = '元兄女人'
for l in lts:
    en = chchr(l)
    print(en)
    print(easy_chord(en))

print('\n'*5)

print(chchr('，'))

print('\n'*5)
st = "我兄弟，我不能做事不管"
for l in st:
    en = chchr(l)
    print(en)

print(encode(st))
