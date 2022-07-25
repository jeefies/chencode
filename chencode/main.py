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
    # print(py)
    e = ''
    punc = punctuation(py)
    # 符号以6开头
    if isinstance(punc, int):
        # use base 7 to avoid 8 appear
        r = '6{}'.format(_basechange(punc)).replace('0', '7')
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

    # 有可能没有音调
    tone = py[-1]
    if tone in digits:
        py = py[:-1]
    else:
        tone = '5'

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

# @witherror
def ordlt(code):
    "Decode one letter's code"
    # print(code)
    # utf-8 letters
    if code.startswith('6'):
        r = chr(int(code[1:].replace('7', '0'), base=7))
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
    if tone == '5':
        tone = ''
    code = code[:-1]

    # 获取到所在的拼音表
    li = nums[int(code[0]) - 1]
    # print(li)
    # 归递获取前两位拼音
    for c in code[1:3]:
        li = li[int(c) - 1]
        # print(li)
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
    result = tuple(ordlt(code) for code in codes.split('0') if code)
    # print(result)
    return result

class DecodeError(Exception): pass

def to_imdata_pixels(codes):
    import math
    try:
        from imdata import ImData
    except ImportError as e:
        print("You must make sure you have installed imdata from pip first!")
        raise e

    try:
        import numpy as np
    except ImportError as e:
        print("How can you install imdata without numpy installed?")
        raise e

    length = len(codes) # length of code
    pixel_rbgs = math.ceil(length / 8) # length of used pixels, exclude chunk data
    content_length = pixel_rbgs  * 3 + 5 # with chunk data

    size = ImData._autosize(content_length) # img size
    imdata_length = ImData._size(size) # number of all pixels (empty pixels included)
    # print(length, pixel_rbgs, content_length, imdata_length, size)

    im = np.zeros(imdata_length, dtype="uint8")
    im[0] = 3
    for i in range(4):
        im[i + 1] = len(codes) & (0xff << (i * 8))

    full_pixels = length // 8 # each pixel has 3 uint8 number
    rest_pixels = length % 8
    # print(full_pixels, rest_pixels)
    for i in range(full_pixels):
        code = int(codes[i * 8 : i * 8 + 8], base=8)
        a, b, c = code & 0xff0000, code & 0x00ff00, code & 0x0000ff
        a = a >> 16
        b = b >> 8
        index = 5 + i * 3
        im[index : index + 3] = np.array([a, b, c], dtype='uint8')
    else:
        if rest_pixels:
            i += 1
            code = int(codes[i * 8 : i * 8 + rest_pixels], base=8)
            a, b, c = code & 0xff0000, code & 0x00ff00, code & 0x0000ff
            index = 5 + i * 3
            im[index : index + 3] = np.array([a >> 16, b >> 8, c], dtype="uint8")

    return im.reshape(size)

def origin_imdata_pixels(im):
    im  = im.reshape(-1)
    imtype = im[0]
    if imtype != 3:
        raise TypeError("Not right chencode imdata!")

    length = 0
    for i in range(4):
        length |= im[i + 1] << (i * 8)

    codes = ''

    full_pixels = length // 8
    rest_pixels = length % 8
    for i in range(full_pixels):
        index = 5 + i * 3
        a, b, c = im[index : index + 3]
        num = (a << 16) | (b << 8) | c
        for i in range(8):
            codes += digits[( num >> (24 - 3 - i * 3) ) & 0b111 ]

    # print(codes, full_pixels, rest_pixels)

    return codes


def _basechange(n, x=7):
    #n为待转换的十进制数，x为进制，取值为2-16
    a = '0123456789ABCDEF'
    b = ''
    while True:
        y = n % x  # 余数
        n = n // x  # 商
        b = a[y] + b
        if n == 0:
            break
    return b
