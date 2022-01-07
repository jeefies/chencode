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

code = main.encode('你好啊，123')
print(code)
imdata = main.to_imdata_pixels(code)
print(imdata)
print(main.decode(main.origin_imdata_pixels(imdata)))
