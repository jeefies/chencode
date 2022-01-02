import  main

r = main.encode('some hello')
print(r)
print(main.decode(r))

r = main.encode('我数据库好地方')
print(r)
print(main.decode(r))

r = main.encode('142857')
print(r)
print(main.decode(r))

r = main.encode(r)
print(r)
print(main.decode(r))
