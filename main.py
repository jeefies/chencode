from pypinyin import pinyin, lazy_pinyin

parts = {1 : {1: 'b', 2 : 'd', 3 : 'p', 4 : 't', 5 : 'y', 6 : 'j'}, 
         2 : {
             1 : { 1 : 'ca', 2 : 'ce', 3 : 'ch', 4 : 'ci', 5 : 'co', 6 : 'cu'},
             2 : {1 : 'sa', 2 : 'se', 3 : 'sh', 4 : 'si', 5 : 'so', 6 : 'su'},
             3 : {1 : 'za', 2 : 'ze', 3 : 'zh', 4 : 'zi', 5 : 'zo', 6 : 'zu'}
            },
         3 : {
             1 : {1 : 'la', 2 : 'le', 3 : 'li', 4 : 'lo', 5 : 'lu', 6 : 'lv'},
             2 : {1 : 'ha', 2 : 'he', 3 : 'hm', 4 : 'hmg', 5 : 'ho', 6 : 'hu'},
             3 : {1 : 'm', 2 : 'ma', 3 : 'me', 4 : 'mi', 5 : 'mo', 6 : 'mu'}
         },
         4 : {
             1 : {1 : 'fa', 2 : 'fe', 3 : 'fo', 4 : 'fu'},
             2 : {1 : 'ga', 2 : 'ge', 3 : 'go', 4 : 'gu'},
             3 : {1 : 'ka', 2 : 'ke', 3 : 'ko', 4 : 'ku'},
             4 : {1 : 'wa', 2 : 'we', 3 : 'wo', 4 : 'wu'}
         },
         5 : {
             1 : 'a',
             2 : 'e',
             3 : 'i',
             4 : 'o',
             5 : 'u'
         }
        }
def chchr(chlt):py = lazy_pinyin(chlt)
