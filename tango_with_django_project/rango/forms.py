from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)  # required=False 表明这个字段不是必须的

    # 嵌套的类，为表单提供额外信息
    class Meta:
        # 把这个 ModelForm 与一个模型连接起来
        # 通过 fields 指定表单中包含哪些字段
        # 通过 excludes 指定排除哪些字段
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=128,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # 把这个 ModelForm 与一个模型连接起来
        model = Page

        # 想在表单中显示哪些字段？
        # 有时不需要全部字段
        # 有些字段接受空值，因此可能无需显示
        # 这里我们想隐藏外键字段
        # 为此，可以排除 category 字段
        exclude = ('category', )
        # 也可以直接指定想显示的字段 (不含 category 字段)
        # fields = ('title', 'url', 'views')

        # 确认/修正用户在表单中输入的数据
        def clean(self):
            cleaned_data = self.cleaned_data    # 表单数据
            url = cleaned_data.get('url')

            # 如果 url 字段不为空，而且不以"http://"开头
            # 在前面加上"http://"
            if url and not url.startwith('http://'):
                url = 'http://' + url
                cleaned_data['url'] = url   # 处理后的新值放回 表单数据

                return cleaned_data