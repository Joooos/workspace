import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

# 导入Django模型(model)之前要导入django, 并把环境变量DJANGO_SETTING_MODULE设为项目的设置文件，然后调用django.setup()，导入项目的设置
# 如果缺少这一步,导入模型时会抛出异常。

import django
django.setup()
from rango.models import Category, Page

def populate():
    # 首先创建一些字典，列出想添加到各分类的网页
    # 然后创建一个嵌套字典，设置各分类
    # 这么做看起来不易理解，但是便于迭代，方便为模型添加数据

    python_pages = [
        {"title": "Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial",
         "views":"1"},
        {"title": "How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/",
         "views": "2"},
        {"title": "Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/",
         "views": "3"} ]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "http://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": "4"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": "5"},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": "6"} ]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/",
         "views": "7"},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": "8"} ]

    user_pages = [
        {"title": "Python.org",
         "url": "https://www.python.org/",
         "views":"9"} ]

    #嵌套字典
    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages},
            "Python User Groups": {"pages": user_pages}}

    # 如果想添加更多分类或网页，添加到前面的字典中即可

    # 下述代码迭代 cats 字典， 添加各分类， 并把相关的网页添加到分类中
    # 迭代字典的正确方式参见
    # http://docs.quantifiedcode.com/python-anti-patterns/readability/

    for cat, cat_data in cats.items():
        # if c.name == 'Python':
        #     c = add_cat(cat, views=128, likes=64)
        # elif c.name == 'Django':
        #     c = add_cat(cat, views=64, likes=32)
        # elif c.name == 'Other Frameworks':
        #     c = add_cat(cat, views=32, likes=16)
        if cat == 'Python':
            c = add_cat(cat, views=128, likes=64)
        elif cat == 'Django':
            c = add_cat(cat, views=64, likes=32)
        elif cat == 'Other Frameworks':
            c = add_cat(cat, views=32, likes=16)
        elif cat == 'Python User Groups':
            c = add_cat(cat, views=16, likes=8)

        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # 打印添加的分类
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]    #get_or_create()方法检查数据库中有没有要创建的记录 后面的[0]表示只返回对象引用
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, likes, views):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.views = views
    c.save()
    return c

# 从这开始执行
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()