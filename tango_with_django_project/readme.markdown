内部tango_with_django_project目录为项目配置目录：

____init____.py：一个空Python脚本，存在目的是告诉Python解释器这个目录是一个Python包

setting.py：存放Django项目的所有设置

urls.py：存放项目的URL模式

wsgi.py：用于运行开发服务器和把项目部署到生产环境的一个Python脚本



另外：

manage.py：它提供了一系列维护Django项目的命令，例如同故宫它可以运行内置的Django开发服务器，可以测试应用，还可以运行多个数据库命令。几乎每个Django命令都要调用这个脚本。