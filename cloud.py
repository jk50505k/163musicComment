import os
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import re

#text=''
# with open('command.txt','r') as fd:
#     for i in fd.readlines():
#         line=i.strip('\n')
#
# text+=' '.join(jieba.cut(line))
comment_text = open('lrc_folk_full.txt','r').read()
comment_text=re.sub(r'\D+：\D+','',comment_text)
comment_text=re.sub(r'\D+ : \D+','',comment_text)
comment_text=re.sub(r'\[\w+\]','',comment_text)
#comment_text=re.sub(r'[a-zA-Z]','',comment_text)#过滤英文
comment_text=re.sub(r'作\w : \D+','',comment_text)

#comment_text=re.sub(r'弦乐 : \D+','',comment_text)
text=''.join(jieba.cut(comment_text))
background=plt.imread('IMG_3674.JPG')#加载背景图片
STOPWORDS.add('原曲')
STOPWORDS.add('作曲')
STOPWORDS.add('作词')
STOPWORDS.add('词曲')
STOPWORDS.add('编曲')
STOPWORDS.add('九九Lrc歌词网')
STOPWORDS.add('制作人')
STOPWORDS.add('九九Lrc')
STOPWORDS.add('99Lrc')
STOPWORDS.add('混音')
STOPWORDS.add('吉他')
STOPWORDS.add('九九歌词网')
STOPWORDS.add('录音')
STOPWORDS.add('后期')
STOPWORDS.add('和声')
STOPWORDS.add('演唱')
STOPWORDS.add('和声编写')
STOPWORDS.add('封面')
STOPWORDS.add('录音室')
STOPWORDS.add('制作')
STOPWORDS.add('原唱')
STOPWORDS.add('翻唱')
wc=WordCloud(
    background_color='white',
    mask=background,
    font_path='/Library/Fonts/Arial Unicode.ttf',
    max_words=2000,
    stopwords=STOPWORDS,
    max_font_size=150,
    random_state=30

)
wc.generate_from_text(text)
print('开始加载文本')
font_colors=ImageColorGenerator(background)
wc.recolor(color_func=font_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()

d=os.path.dirname(__file__)

wc.to_file(os.path.join(d,'lrc_folk_full(英文).jpg'))
print('success')