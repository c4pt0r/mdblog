<!-- First Post -->
<!-- 2013-10-06 22:23:13 -->
<!-- write markdown text below  -->
#First Post

在尝试过各种Blog平台后，我仍然没有养成写Blog的良好习惯，我将这归咎于Blog本身的问题 (-_-||, 没错，就是传说中的拉不出屎怪茅坑)。细数一下，我在以下平台上都尝试留过文字:

* WordPress
* Jekyll
* MDWiki
* Writings.io, 简书
* CSDN, 163, cnblog等各种商用平台
* ...

但都不幸的失败了, 失败的原因多种多样, 比如:

* 不支持markdown
* 不支持代码高亮
* 样子太丑（没错，我是极简主义者）
* 不支持自定义的域名

终于我忍无可忍了，在一个闲得蛋疼的晚上，有了这个东西 -- MDBlog

这个简单的脚本做的事情很简单，就是读取.md文件，按照模板生成.html文件，然后丢到服务器上做静态文件服务.

顺手就开源了，也不是什么高科技的东西，开源的唯一目的是需要用github来存档, 如果有被各种乱七八糟的模板搞烦的同鞋，可以玩玩:

Github: [https://github.com/c4pt0r/mdblog/](https://github.com/c4pt0r/mdblog/)


##usage:

    build.py new
    创建新文章
    build.py build
    生成站点


##文件夹们

###./template

放置模板文件，其中blog.html是正文的模板, index.html是首页的模板

###./static

静态文件目录，图片css什么的放在这里, build的时候会直接拷贝到gen目录下

###./blogs

博客文章.md格式文件存放的位置, 需要满足如下格式:

    <!-- 标题 -->
    <!-- 日期 e.g. 2013-10-01 12:00:00 -->
    ...

如：

    <!-- Hello World  -->
    <!-- 2013-10-01 12:00:00 -->
    #Hello World
    ## hello world!

