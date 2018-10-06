内部tango_with_django_project目录为项目配置目录：

____init____.py：一个空Python脚本，存在目的是告诉Python解释器这个目录是一个Python包

admin.py：注册模型，让Django为你创建管理界面

apps.py：当前应用的配置

models.py：存放应用的数据模型，即数据的实体及其之间的关系

tests.py：存放测试应用代码的函数

views.py：存放处理请求并返回响应的函数

migrations目录：存放与模型有关的数据库信息

views.py和models.py是任何应用中都有的两个文件，是Django所采用的设计模式（模型-视图-模板）的主要部分



另外：

manage.py：它提供了一系列维护Django项目的命令，例如同故宫它可以运行内置的Django开发服务器，可以测试应用，还可以运行多个数据库命令。几乎每个Django命令都要调用这个脚本。