from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm

#在views.py中，一个函数就是一个视图，视图函数至少有一个参数，即一个HttpRequest对象，还必须返回一个HttpResponse对象

from django.http import HttpResponse

def index(request):
    # return HttpResponse("Rango says hey there partner!<br/> <a href='/rango/about/'>About</a>")
    # 构建一个字典，作为上下文传给模板引擎
    # 注意，boldmessage 键对应于模板中的 {{ boldmessage }}
    #context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # 查询数据库，获取目前存储的所有分类
    # 按点赞次数倒序排列分类
    # 获取前5个分类(如果分类数少于5个， 那就获取全部)
    # 把分类列表放入 context_dict 字典
    # 稍后传给模板引擎
    category_list = Category.objects.order_by('-likes')[:5]     # - 号表示倒序，没有则表示升序，这里返回一个Category对象子集
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}

    # 返回一个渲染后的相应发给客户端
    # 为了方便，我们使用的是render 函数的简短形式
    # 注意，第二个参数是我们想使用的模板
    # render函数三个参数，请求对象/模板文件名/上下文字典
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>Index</a>")
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})

def show_category(request, category_name_slug):
    # 创建上下文字典，稍后传给模板渲染引擎
    context_dict = {}

    try:
        # 能通过传入的分类别名找到对应的分类吗?
        # 如果找不到， .get()方法 抛出DoesNotExist 异常
        # 因此 .get()方法返回一个模型实例或抛出异常
        category = Category.objects.get(slug=category_name_slug)

        # 检索关联的所有网页
        # 注意， filter()返回一个网页对象列表或空列表
        pages = Page.objects.filter(category=category)

        # 把得到的列表赋值给模板上下文中名为 pages 的键
        context_dict['pages'] = pages
        # 也把从数据库中获取的 category 对象添加到上下文字典中
        # 我们将在模板中通过这个变量确认分类是否存在
        context_dict['category'] = category

    except Category.DoesNotExist:
        # 没找到指定的分类时执行这里
        # 什么也不做
        # 模板会显示消息，指明分类不存在
        context_dict['category'] = None
        context_dict['pages'] = None

    # 渲染响应，返回给客户端
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # 是 HTTP POST 请求吗?
    if request.method == 'POST':    # 检查是不是HTTP POST请求，即是不是通过表单提交的数据
        form = CategoryForm(request.POST)

        # 表单数据有效吗?
        if form.is_valid():
            # 把新分类存入数据库
            form.save(commit=True)
            # 保存新分类后可以显示一个确认信息
            # 不过既然最受欢迎的分类在首页
            # 那就把用户带到首页吧
            return index(request)
        else:
            # 表单数据有错误
            # 直接在终端里打印出来
            print(form.error)

    # 处理有效数据和无效数据之后
    # 渲染表单，并显示可能出现的错误信息
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
            # form.save(commit=True)
            # return index(request)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # 告诉模板注册是否成功
    registered = False

    if request.method == 'POST':
        # 获取原始表单数据
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # 数据有效
        if user_from.is_valid() and profile_form.is_valid():
            # 把 UserForm 中的数据存入数据库
            user = user_form.save()

            # 使用set_password 方法计算密码哈希值
            # 然后更新 user 对象
            user.set_password(user.password)
            user.save()

            # 处理UserProfile 实例
            # 因为要自行处理 user 属性，所以设定commit=False
            # 延迟保存模型，以防出现完整性问题
            profile = profile_form.save(commit=False)
            profile.user = user

            # 头像文件
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # 保存
            profile.save()

            # 更新变量的值，告诉模板成功注册了
            registered = True

        else:
            # 表单数据无效
            # 打印问题
            print(user_form.errors, profile_form.errors)
    else:
        # 不是 HTTP POST 请求， 渲染两个 ModelFrom 实例
        # 表单为空，待用户填写
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   registered: registered})












