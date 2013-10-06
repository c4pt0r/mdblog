mdblog
======

simple blog generate script

我的博客生成的脚本


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

  
