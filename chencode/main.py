from .lts import lts, nums, letters, bletters, yun, yunb
from string import punctuation as spuncs
from string import whitespace, digits
from functools import wraps

from pypinyin import pinyin, Style


# Eng punctuation and whitespaces
sws = spuncs + whitespace


def chrlt(lt):
    "Encode one letter"
    py = pinyin(lt, style=Style.NORMAL)[0][0]
    if py == lt:
        return '6{:o}'.format(punctuation(lt))
    return _encode(py)

def punctuation(lt):
    """Check if the letter is a punctuation"""
    #Chinese in 4e00 - 9fef
    if '\uff01' <= lt <= '\uff5e':
        return ord(lt) - 65248
    elif '\u3000' == lt:
        return 32
    elif lt == '\u3002':
        return 46
    elif lt == '\u3001':
        return 44
    elif lt in sws:
        return ord(lt)
    return lt

# encode one letter, only one (has changed to pinyin)
def _encode(py):
    "Encode one letter which has changed to pinyin already"
    py = py.lower()
    e = ''
    punc = punctuation(py)
    if isinstance(punc, int):
        r = '6{:o}'.format(punc).replace('0', '8')
        return r

    if py in digits:
        return py

    if len(py) == 1:
        return letters[py]

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

# The function to show where the error is raised (which code)
def witherror(func):
    ("Show The error with the code to decode\n"
            "Raise a Decode Error Then")
    @wraps(func)
    def wrapper(code):
        try:
            return func(code)
        except Exception:
            raise DecodeError("Error When Decoding %s" % code, code)
    return wrapper

@witherror
def ordlt(code):
    "Decode one letter's code"
    # utf-8 letters
    if code.startswith('6'):
        r = chr(int(code[1:].replace('8', '0'), base=8))
        return r

    # single number
    if len(code) == 1:
        return code

    # single letter(Eng letters)
    if len(code) == 2:
        return bletters[code]

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
    "Encode a string, a few letters (Eng letters, Chinese words, numbers)"
    py = lambda stri: pinyin(stri, style=Style.NORMAL)[0]
    return '0'.join(_encode(i[0]) for i in map(py, string))

def decode(codes):
    ("Decode the result of the encode to the"
            " similar words from the origin sentence\n"
            "Such as lower cases, and pinyin of the Ch words"
            )
    return tuple(ordlt(code) for code in codes.split('0'))

class DecodeError(Exception): pass
