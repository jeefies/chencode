'''
All the letters indexes
but need to add one to each index
'''
nums = [
        [ #0
            'ba be bi bo bu'.split(),
            'da de di do du'.split(),
            'pa pe pi po pu'.split(),
            'ta te ti to tu'.split(),
            'ya ye yi yo yu'.split(),
            'ja je ji jo ju'.split(),
        ],
        [ #1
            'ca ce ch ci co cu'.split(),
            'sa se sh si so su'.split(),
            'za ze zh zi zo zu'.split(),
        ],
        [ #2
            'la le li lo lu lv'.split(),
            'ha he hm hmg ho hu'.split(),
            'm ma me mi mo mu'.split(),
        ],
        [ #3
            'fa fe fo fu'.split(),
            'ga ge go gu'.split(),
            'ka ke ko ku'.split(),
            'wa we wo wu'.split(),
            'ra re ri ro ru'.split(),
            'xa xe xi xo xu'.split(),
            'qa qe qi qo qu'.split(),
        ],
        [ #4
            ['aa', 'ae', 'ai', 'ao', 'au', 'an', 'ang'],
            ['ea', 'er', 'ei', 'eo', 'eu', 'en', 'eng'],
            'i',
            'o',
            'u',
            'na ne ni no nu nv'.split(),
            'ng'
        ]
    ]

lts = {
   'ba':'111', 'be':'112', 'bi':'113', 'bo':'114', 'bu':'115',
   'da':'121', 'de':'122', 'di':'123', 'do':'124', 'du':'125',
   'pa':'131', 'pe':'132', 'pi':'133', 'po':'134', 'pu':'135',
   'ta':'141', 'te':'142', 'ti':'143', 'to':'144', 'tu':'145',
   'ya':'151', 'ye':'152', 'yi':'153', 'yo':'154', 'yu':'155',
   'ja':'161', 'je':'162', 'ji':'163', 'jo':'164', 'ju':'165',

   'ca':'211', 'ce':'212', 'ch':'213', 'ci':'214', 'co':'215', 'cu':'216',
   'sa':'222', 'se':'222', 'sh':'223', 'si':'224', 'so':'225', 'su':'226',
   'za':'231', 'ze':'232', 'zh':'233', 'zi':'234', 'zo':'235', 'zu':'236',

   'la':'311', 'le':'312', 'li':'313', 'lo':'314', 'lu':'315', 'lv':'316',
  'ha':'321', 'he':'322', 'hm':'323', 'hmg':'324', 'ho':'325', 'hu':'326',
   'm':'331', 'ma':'332', 'me':'333', 'mi':'334', 'mo':'335', 'mu':'336',

   'fa':'411', 'fe':'412', 'fo':'413', 'fu':'414',
   'ga':'421', 'ge':'422', 'go':'423', 'gu':'424',
   'ka':'431', 'ke':'432', 'ko':'433', 'ku':'434',
   'wa':'441', 'we':'442', 'wo':'443', 'wu':'444',
   'ra':'451', 're':'452', 'ri':'453', 'ro':'454', 'ru':'455',
   'xa':'461', 'xe':'462', 'xi':'463', 'xo':'464', 'xu':'465',
   'qa':'471', 'qe':'472', 'qi':'473', 'qo':'474', 'qu':'475',

   'na':'561', 'ne':'562', 'ni':'563', 'no':'564', 'nu':'565', 'nv': '566',
   'er':'522', 'en':'526', 'ei':'523', 'eng':'527',
   'ai':'513', 'ao':'514',
    }

yun = dict(zip('a e i o u n ng'.split(), map(str, range(1, 8))))
yunb = {v:k for k,v in yun.items()}


letters = {
   'b':'11',
   'd':'12',
   'p':'13',
   't':'14',
   'y':'15',
   'j':'16',

   'c':'21',
   's':'22',
   'z':'23',

   'l':'31',
   'h':'32',
   'm':'33',

   'f':'41',
   'g':'42',
   'k':'43',
   'w':'44',
   'r':'45',
   'x':'46',
   'q':'47',

   'n':'56',
   'e':'52',
   'i':'53',
   'a':'51',
   'o':'54',
   'u':'55',

   'v':'34',
   ' ':'24',
    }

bletters = {v:k for k, v in letters.items()}
