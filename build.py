#!/usr/bin/env python
import shutil
import json
import os
import sys
import markdown
import glob
import time
def pre_check():
    paths = ['./blogs', './template/blog.html', './template/index.html']
    for p in paths:
        if not os.path.exists(p):
            return False, p
    return True, None

def write_file(file_name, content):
    fp = open(file_name, 'w')
    fp.write(content)
    fp.close()

def is_markdown_comment(line):
    if line.startswith('<!--') and line.endswith('-->'):
        return True
    return False

def get_comment_text(markdown_comment):
    return markdown_comment.replace('<!--', '').replace('-->', '').lstrip().rstrip()

def new_post():
    title = raw_input('title (e.g. Hello World): ')
    file_name = raw_input('filename without extension (e.g. hello_world): ')

    try:
        os.mkdir('./blogs')
    except:
        pass

    fp = open('./blogs/' + file_name + '.md', 'w')
    title = '<!-- '+ title +' -->'
    date_str = '<!-- ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' -->'
    fp.write(title + '\n')
    fp.write(date_str + '\n')
    fp.write('<!-- write markdown text below  -->')
    fp.close()
    os.system('vim ' + './blogs/' + file_name + '.md')

def build():
    shutil.rmtree('./gen')
    os.mkdir('./gen')
    blogs = []
    for f in glob.glob('./blogs/*.md'):
        fp = open(f)
        content = fp.read()
        fp.close()
        if len(content.split('\n')) < 3:
            print 'invalid post -1', f
            continue
        #first line is datetime string, get it
        title = content.split('\n')[0]
        date_str = content.split('\n')[1]
        if is_markdown_comment(title) == False or is_markdown_comment(date_str) == False:
            print 'invalid post -2', f
            continue

        title = get_comment_text(title)
        date_str = get_comment_text(date_str)
        md_content = '\n'.join(content.split('\n')[2:])
        try:
            ts = time.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            content = md_content
        except:
            ts = time.localtime()
        html = markdown.markdown(content)
        if len(html) == 0:
            continue
        #generate blog html
        blog_fp = open('./template/blog.html')
        content = blog_fp.read()
        content = content.replace('{{ blog }}', html)

        file_name = os.path.basename(f)
        file_name, _ = os.path.splitext(file_name)
        write_file('./gen/' + file_name + '.html', content)
        print 'write', file_name, '...done'
        blogs.append((file_name + '.html', title, ts))
        blog_fp.close()
    #generate index html
    index_fp = open('./template/index.html')
    content = index_fp.read()
    blogs.sort(key=lambda b: b[2])
    blogs.reverse()
    html = ''
    for url, title, ts in blogs:
        date_str = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        line = '<div class="post-item"><a href="%s">%s</a><span>%s</span></div>' % (url, title, date_str)
        html = html + line + '\n'

    content = content.replace('{{ bloglist }}', html)
    write_file('./gen/index.html', content)
    print 'write index ...done'

    #copy static files
    if os.path.exists('./static'):
        shutil.copytree('./static', './gen/static')
        print 'copy static files ...done'

if __name__ == '__main__':
    b, p = pre_check()
    if not b:
        print p, 'not exists!'
        exit(-1)
    if len(sys.argv) < 2:
        print 'argument missing'
        print 'build.py [build|new]'
        exit(-2)
    if sys.argv[1].lower() == 'build':
        build()
    elif sys.argv[1].lower() == 'new':
        new_post()
