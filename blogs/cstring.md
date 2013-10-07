<!-- 论如何设计一个简单的C字符串库 -->
<!-- 2013-10-07 11:33:27 -->
<!-- write markdown text below  -->
#论如何设计一个简单的C字符串库

其实这个作为面试题还是一个不错的题目, 我至少在很多的地方见过类似的, 不过基本以模仿STL的std::string为目标的C++题目。但我们今天讨论的是C。

云风在他的[blog](http://blog.codingnow.com/2013/09/cstring.html)里提到， 他的cstring主要特点是：

1. 尽量减少字符串在堆上的动态内存分配， 尽量在栈上使用
2. 短字符串做interning, interning pool不做释放

实现没得说，代码写得很漂亮, 但是我仍然觉得略繁琐，在一般的项目中其实很难做到这个级别的优化，不过如果有当然很棒。

顺便提一下redis的sds的设计。

sds本身就是一个char*，没有什么的特别的，而它的meta信息全部存储于sdshdr结构体中：

    typedef char *sds;
    struct sdshdr {
        int len;
        int free;
        char buf[];
    };
    
    +----------------------------------------+
    |   len   |   free  |         buf        |
    +----------------------------------------+
    |                   |
    sdshdr             sds
    

当我们通过sdsnewlen创建一个字符串的时候，我们得到的是一个sds的指针，也就是一个char*，标准的c字符串, 但是我们如果需要释放或者访问hdr内部的结构呢? 

这里用到一个创建可变长结构体的技巧, 注意sdshdr的最后一个成员char buf[]，将最后一个成员声明为可变数组(char[])类型，此时这个结构体就是一个可变长的结构体. 在计算sizeof(struct sdshdr)的时候长度为len和free所占的空间，也就是sizeof(int) * 2，

可变数组虽然看上去像一个指针，但是和char*不同的是，并不会占sizeof结构体的空间.

于是，我们只需要拿到sds类型的指针, 虽然上去是一个char*，但是我们知道它其实指向的是sdshdr->buf, 只需要将这个指针向前移动 sizeof(struct sdshdr)的大小, 即可取得整个sdshdr对象的地址。下面给出sdsnewlen的实现，

    sds sdsnewlen(const void *init, size_t initlen) {
        struct sdshdr *sh;
        sh = malloc(sizeof(struct sdshdr)+initlen+1); // here
        if (sh == NULL) return NULL;
        sh->len = initlen;
        sh->free = 0;
        if (initlen) {
            if (init) memcpy(sh->buf, init, initlen);
            else memset(sh->buf,0,initlen);
        }
        sh->buf[initlen] = '\0';
        return (char*)sh->buf; // here
    }

