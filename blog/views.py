from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
# Create your views here.
from . import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Article
from .forms import PostForm


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated():    #验证用户是否存在
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)  # 绑定form里的PostForm函数，
    if form.is_valid():  # 验证表单是否有效
        instance = form.save(commit=False)  # save保存函数，成为实例
        instance.user = request.user  # 实例用户
        # print(form.cleaned_data.get("title"))  # 表单验证成功后的数据保存到cleaned_data里
        instance.save()  # 保存实例
        messages.success(request, '文章发布完成!')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request, '文章发布失败!')
    # if request.method == 'POST':
    #     print(request.POST.get('content'))
    #     title=request.POST.get('title')
    #     Article.objects.create(title=title) #自带的提交函数
    #     print('表单已提交')
    context = {'form': form}
    return render(request, 'post_form.html', context)


def post_detail(request, slug=None):
    # instance = Article.objects.get(id=1)
    instance = get_object_or_404(Article, slug=slug)  # 取得obj或显示404
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    context = {'title': instance.title, 'instance': instance}
    return render(request, 'post_detail.html', context)


# @login_required
def post_list(request):
    today = timezone.now().date()  # 当前时间

    queryset_list = Article.objects.active()  # order_by('-timestamp')
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Article.objects.all()  # order_by('-timestamp')
    query = request.GET.get("q")  # 查询请求
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(
                content__icontains=query)|Q(publish__contains=query)).distinct() #去重复
    paginator = Paginator(queryset_list, 5)  # 控制显示数量

    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {'object_list': queryset, 'title': '魏大大', 'today': today}
    return render(request, 'post_list.html', context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Article, slug=slug)  # 取得obj或显示404
    form = PostForm(request.POST or None, request.FILES or None,
                    instance=instance)  # 绑定form里的PostForm函数，instance用来显示现在的实例
    if form.is_valid():  # 验证表单是否有效
        instance = form.save(commit=False)  # save保存函数，成为实例
        # print(form.cleaned_data.get("title"))  # 表单验证成功后的数据保存到cleaned_data里
        instance.save()  # 保存实例
        messages.success(request, '<a href="#">编辑</a>成功', extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())  # 重新定向函数HttpResponseRedirect
    context = {'title': instance.title, 'instance': instance, 'form': form}
    return render(request, 'post_form.html', context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Article, slug=slug)  # 取得obj或显示404
    instance.delete()
    messages.success(request, '删除成功')
    return redirect('blog:list')
