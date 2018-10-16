# 163musicComent
抓取网易云音乐下某个类目下的音乐的评论进行词频分析生成词云
## 依赖
[用到的免费ip池@hao104/proxy_pool](https://github.com/jhao104/proxy_pool)
wordcloud jieba
## 原理  
搜索关键词对应类目的歌单，选取多个（自定数量）歌单，抓取歌单内所有歌曲的用户评论<br>
里面也可调用歌词抓取的函数（getLyric）进行分析<br>
再利用jieba,wordcloud库进行词频分析
## 使用效果

