from pypinyin import pinyin, Style


FULL = Style.TONE3
ONLY = Style.NORMAL

parts = {1: {1: 'b', 2: 'd', 3: 'p', 4: 't', 5: 'y', 6: 'j'},
         # key 1, for the first letter with aeiou except y and j are special
         2: {  # key 2, especially for c, s, z can be used like ch, zh, sh
             1: {1: 'ca', 2: 'ce', 3: 'ch', 4: 'ci', 5: 'co', 6: 'cu'},
             2: {1: 'sa', 2: 'se', 3: 'sh', 4: 'si', 5: 'so', 6: 'su'},
             3: {1: 'za', 2: 'ze', 3: 'zh', 4: 'zi', 5: 'zo', 6: 'zu'}
},
    3: {  # key 3, can have 6 way to connect with next letter
             1: {1: 'la', 2: 'le', 3: 'li', 4: 'lo', 5: 'lu', 6: 'lv'},
             2: {1: 'ha', 2: 'he', 3: 'hm', 4: 'hmg', 5: 'ho', 6: 'hu'},
             3: {1: 'm', 2: 'ma', 3: 'me', 4: 'mi', 5: 'mo', 6: 'mu'},
},
    4: {  # key 4, only has 4 way to connect with next letter, special for r, x
             1: {1: 'fa', 2: 'fe', 3: 'fo', 4: 'fu'},
             2: {1: 'ga', 2: 'ge', 3: 'go', 4: 'gu'},
             3: {1: 'ka', 2: 'ke', 3: 'ko', 4: 'ku'},
             4: {1: 'wa', 2: 'we', 3: 'wo', 4: 'wu'},
             5: 'r',
             6: 'x'
},
    5: {  # other specials
             1: 'a',
             2: 'e',
             3: 'i',
             4: 'o',
             5: 'u',
             6: 'n',
             7: 'ng'
},
    6: {i+1: v for i, v in enumerate('na ne ng ni no nu nv'.split())},
    7: {i+1: l for i, l in enumerate('，。？！、～—')}
}

enparts = {  # the encode rule for the letters
    'b': (1, 1), 'd': (1, 2), 'p': (1, 3),
    't': (1, 4), 'y': (1, 5), 'j': (1, 6),
    'ca': (2, 1, 1), 'ce': (2, 1, 2), 'ch': (2, 1, 3),
    'ci': (2, 1, 4), 'co': (2, 1, 5), 'cu': (2, 1, 6),
    'sa': (2, 2, 1), 'se': (2, 2, 2), 'sh': (2, 2, 3),
    'si': (2, 2, 4), 'so': (2, 2, 5), 'su': (2, 2, 6),
    'za': (2, 3, 1), 'ze': (2, 3, 2), 'zh': (2, 3, 3),
    'zi': (2, 3, 4), 'zo': (2, 3, 5), 'zu': (2, 3, 6),
    'ng': (5, 7),
    'x': (4, 6),
    'r': (4, 5),
}
enparts.update({l: (3, 1, n + 1)
                for n, l in enumerate('la le li lo lu lv'.split())})
enparts.update({l: (3, 2, n + 1)
                for n, l in enumerate('ha he hm hmg ho hu'.split())})
enparts.update({l: (3, 3, n + 1)
                for n, l in enumerate('m ma me mi mo mu'.split())})
for a, p in enumerate('fgkw'):
    enparts.update({l: (4, a + 1, b + 1)
                    for b, l in enumerate(map(lambda x: p + x, 'aeou'))})
enparts.update({l: (5, a + 1) for a, l in enumerate('aeioun')})
enparts.update({l: (6, a + 1)
                for a, l in enumerate('na ne ng ni no nu nv'.split())})
enparts.update({l: (7, i + 1) for i, l in enumerate('，。？！～—')})
dots = '，。？！～—'


class Dict(dict):
    def getift(self, tup):
        if isinstance(tup, int):
            return self[tup]
        length = len(tup)
        if length == 3:
            return self[tup[0]][tup[1]][tup[2]]
        elif length == 2:
            return self[tup[0]][tup[1]]
        elif length == 1:
            return self[tup[0]]
        else:
            raise OverflowError('length of the tuple overflowed')

    def gets(self, stri):
        return self.getift(tuple(map(int, stri)))


parts = Dict(parts)
enyuan = {l: i + 1 for i, l in enumerate('aeioun')}
yuan = {str(l): i for i, l in enyuan.items()}
yuan.update({str(7): 'ng'})


def easy_chchr(chlt):
    py = pinyin(chlt, style=ONLY)[0][0]
    return str(int(_encode(py), base=8))


def _encode(py):
    # start encode for first one or two letter

    if py in dots:
        return ''.join(map(str, enparts[py]))
    p0 = py[0]

    if p0 in 'bdptyjxraeiou':  # if it's the special letter
        r = enparts[p0]
        py = py[1:]
    else:  # the first to letter is in the encode rule dict
        r = enparts[py[:2]]
        py = py[2:]

    m = ()  # the letter in the middle
    end = ()  # the last letter's num
    if py.endswith('ng'):
        end = (7, )
        py = py[:-2]
    if py:
        m = tuple(enyuan[p] for p in py)
    return ''.join(map(str, r + m + end))


def encode(sent, style=ONLY):
    if style not in (ONLY, FULL):
        raise TypeError('No support style')
    piny = sum(pinyin(sent, style=style), [])
    en = _encode
    return int('0'.join(str(en(py)) for py in piny), base=8)


def easy_chord(chen):
    stri = oct(int(chen))[2:]
    return _decode(stri)


def _decode(s):
    s0 = s[0]
    if s0 in '15':
        t = parts.gets(s[:2])
        s = s[2:]
    elif s0 == '7':
        return parts.gets(s)
    else:
        s2 = s[:2]
        if s2 in ('45', '46'):
            t = parts.gets(s2)
            s = s[2:]
        else:
            t = parts.gets(s[:3])
            s = s[3:]
    if s:
        m = ''.join(yuan[lt] for lt in s)
    else:
        m = ''
    return t + m
