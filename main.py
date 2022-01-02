try:
    from .lts import lts, nums, letters, bletters, yun, yunb
except ImportError:
    from lts import lts, nums, letters, bletters, yun, yunb
from string import punctuation as spuncs
from string import whitespace, digits
from functools import wraps

from pypinyin import pinyin, Style


# Eng punctuation and whitespaces
sws = spuncs + whitespace + digits


def chrlt(lt):
    "Encode one letter"
    py = pinyin(lt, style=Style.TONE3)[0][0]
    if py == lt:
        return '6{:o}'.format(punctuation(lt))
    return _encode(py)

def punctuation(lt):
    """Check if the letter is a punctuation"""
    #Chinese in 4e00 - 9fef
    # 检查是否为符号，中文符号将转为半角
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
    # 编码一个字符，产生一个8进制数，此种，8为0
    py = py.lower()
    e = ''
    punc = punctuation(py)
    # 符号以6开头
    if isinstance(punc, int):
        r = '6{:o}'.format(punc).replace('0', '8')
        return r

    # 如果为数字，则直接返回数字
    if py in digits:
        return py

    # 如果拼音只有一个，则直接从列表里返回对应值
    # 如果是单个英文字符，也是
    if len(py) == 1:
        return letters[py]

    # 处理特殊的音符
    if py[:3] == 'hmg':
        return lts[py]

    #print(py)
    tone = py[-1]
    py = py[:-1]
    # 前两个字符可以直接匹配
    if len(py) == 2:
        return lts[py] + tone
    # 后面的字符就在前面的基础上叠加
    ft = lts[py[:2]] # first two code

    # ng是特殊的音节，只占一位数字
    if py.endswith('ng'):
        py = py[:-2]
        e = '7'

    # 处理中间的拼音，至多3个
    m = ''.join(yun[i] for i in py[2:])
    return ft + m + e + tone

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
    #print(code)
    # utf-8 letters
    if code.startswith('6'):
        r = chr(int(code[1:].replace('8', '0'), base=8))
        return r

    # single number
    # 单个数字
    if len(code) == 1:
        return code

    # single letter(Eng letters)
    # 单个字母或者是单个拼音
    if len(code) == 2:
        return bletters[code]

    # 将音调与拼音分离
    tone = code[-1]
    code = code[:-1]

    # 获取到所在的拼音表
    li = nums[int(code[0]) - 1]
    # 归递获取前两位拼音
    for c in code[1:3]:
        li = li[int(c) - 1]
    ft = li

    # 若是只有两个，则直接返回
    if len(code) == 3:
        return ft + tone

    # 将剩下的加入其中
    for c in code[3:]:
        ft += yunb[c]
    return ft + tone


def encode(string):
    "Encode a string, a few letters (Eng letters, Chinese words, numbers)"
    py = lambda stri: pinyin(stri, style=Style.TONE3)[0]
    return '0'.join(_encode(i[0]) for i in map(py, string))

def decode(codes):
    ("Decode the result of the encode to the"
            " similar words from the origin sentence\n"
            "Such as lower cases, and pinyin of the Ch words"
            )
    return tuple(ordlt(code) for code in codes.split('0'))

class DecodeError(Exception): pass
