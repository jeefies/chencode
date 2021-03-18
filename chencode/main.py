try:
    from .lts import lts, nums, yun, yunb
except ImportError:
    from lts import lts, nums, yun, yunb
from pypinyin import pinyin, Style

#pprint = __import__('pprint').pprint
#pprint(yun)
#pprint(lts);pprint(nums)

def chrlt(lt):
    py = pinyin(lt, style=Style.NORMAL)[0][0]
    if py == lt:
        return '6{:o}'.format(punctuation(lt))
    return _encode(py)

def punctuation(lt):
    #Chinese in 4e00 - 9fef
    if not len(lt) == 1:
        return lt
    if '\uff01' <= lt <= '\uff5e':
        return ord(lt) - 65248
    elif '\x20' <= lt <= '\x7e':
        return ord(lt)
    elif '\u3000' == lt:
        return 32
    elif lt == '\u3002':
        return 46
    elif lt == '\u3001':
        return 44
    elif '\x20' <= lt <= '\x7e':
        return ord(lt)
    return lt

def _encode(py):
    print(repr(py), len(py))
    e = ''
    punc = punctuation(py)
    if isinstance(punc, int):
        return '6{:o}'.format(punc)
    if len(py) == 1:
        try:
            return '5' + yun[py]
        except KeyError:
            return '6%o' % ord(py)
    if py == 'hmg':
        return lts[py]
    if len(py) == 2:
        return lts[py]
    ft = lts[py[:2]] # first two code
    if py.endswith('ng'):
        py = py[:-2]
        e = '7' + e
    m = ''.join(yun[i] for i in py[2:])
    return ft + m + e

def ordlt(code):
    if code.startswith('6'):
        return chr(int(code[1:], base=8))
    li = nums[int(code[0]) - 1]
    for c in code[1:3]:
        li = li[int(c) - 1]
    ft = li
    if len(code) == 3:
        return ft
    for c in code[3:]:
        ft += yunb[c]
    return ft

def encode(string):
    py = lambda stri: pinyin(stri, style=Style.NORMAL)[0]
    return '0'.join(_encode(i[0]) for i in map(py, string))

def decode(codes):
    return ' '.join(ordlt(code) for code in codes.split('0'))


if __name__ == '__main__':
    print(chrlt('，'))
    for c in '诶我是你儿子滚远一点':
        cc = chrlt(c)
        print(cc, end=' ')
        print(ordlt(cc))

    code = encode('你好啊上班,组')
    print(code)
    print(decode(code))
