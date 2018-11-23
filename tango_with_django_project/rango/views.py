from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
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
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]     # - 号表示倒序，没有则表示升序，这里返回一个Category对象子集
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': page_list}

    # 调用处理 cookie 的辅助函数
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # 返回一个渲染后的相应发给客户端
    # 为了方便，我们使用的是render 函数的简短形式
    # 注意，第二个参数是我们想使用的模板
    # render函数三个参数，请求对象/模板文件名/上下文字典
    # 提前获取 response 对象， 以便添加 cookie
    response = render(request, 'rango/index.html', context=context_dict)

    # 返回 response 对象， 更新目标 cookie
    return response

def about(request):
    #return HttpResponse("Rango says here is the about page.<br/> <a href='/rango/'>Index</a>")
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    print(request.method)
    print(request.user)
    visitor_cookie_handler(request)
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)

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
        if user_form.is_valid() and profile_form.is_valid():
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

def user_login(request):
    if request.method == 'POST':
        # 获取用户在登录表单中输入的用户名和密码
        # 我们使用的是 request.POST.get('<variable>')
        # 而不是 request.POST('<variable>')
        # 这是因为对应的值不存在时，前者返回 None，后者抛出 KeyError 异常
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 使用Django提供的函数检查 username/password 是否有效
        # 有效的话返回一个 User 对象
        user = authenticate(username=username, password=password)

        # 如果得到了 User 对象
        # 如果是 None， 说明没找到与凭据匹配的用户
        if user:
            # 账户激活了
            if user.is_active:
                # 登入账户
                # 然后重定向到首页
                login(request, user)
                return HttpResponseRedirect(reverse('index'))   # reverse 函数在 Rango 应用的 urls.py 模块中查找名为 index 的 URL模式，解析出对应的 URL
            else:
                # 账户未激活，禁止登录
                return HttpResponse("Your Rango account is disabled.")

        else:
            # 提供的登录凭据有问题，不能登录
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.用户名或密码错误")


    # 不是 HTTP POST 请求，显示登录表单
    # 极有可能是 HTTP GET 请求
    else:
        # 没什么上下文变量要传给模板系统
        # 因此传入一个空字典
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    #return HttpResponse("Since u're logged in, u can see this text!")
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#辅助函数
def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# 不是视图函数，是辅助函数，因为它不返回 response 对象
def visitor_cookie_handler(request):
    # 获取网站的访问次数
    # 使用 COOKIES.get() 函数读取"visits" cookie
    # 如果目标 cookie 存在，把值转换为整数
    # 如果目标 cookie 不存在， 返回默认值 1

    # visits = int(request.COOKIES.get('visit','1'))
    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    # 改成从服务器端存取 cookie
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # 如果距上次访问已超过一天....
    if (datetime.now() - last_visit_time).days > 0: # .days 改成 .seconds 只要相差一秒就能更新访问次数
        visits = visits + 1
        # 增加访问次数后更新 "last_visit" cookie
        # response.set_cookie('last_visit', str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
        #response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie

    #response.set_cookie('visits', visits)
    request.session['visits'] = visits



