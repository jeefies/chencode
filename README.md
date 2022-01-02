# Ch encode
**Author: Jeefy**  
**Email: jeefyol@outlook.com / jeeefy163@163.com**  

The encode rule for encoding a chinese letter.  
According to the pinyin of a letter 

## RULE
- Chinese Words  
Use `pypinyin` to convert each letter into a pinyin.  
Notice that, there's no Chinese TONE here.  
So you just can guess what you have written by yourself.  
- English Words_
It's all can decode back to origin.  
- Punctuations  
Notice that the Chinese punctuations would change to English punctuations.  
- Specials  
The specials letters will convert into unicode number, and then save as the code starts with '6'.  
The followed codes are the number based on base 8 (0 -> 8).  

## Notice
It's not wise to encode a numeric str!
It will be 4 times longer!

## GUI
**The gui can be opened with `python -m chencode`**  
Remember you should call it under the readme file folder.  
The template for the text editor will fork into another package.  
Waiting for the docs then...
