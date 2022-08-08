from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import numpy as np
# Create your views here.


# 个人中心主页
from django.urls import reverse

from searchcenter.models import SearchHistory, SchoolInfo, CntToUrl
from usercenter.models import ArticleInfo, ArticleTag, CollectionInfo


@login_required(login_url='/login')
def indexView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        personalInfo = request.POST.get('personalInfo')
        address = request.POST.get('address')
        photo = request.FILES.get('fileupload')
        user = request.user
        if user:
            user.username = username
            user.name = name
            user.email = email
            user.telephone = telephone
            user.introduce = personalInfo
            user.address = address
            user.photo = photo
            user.save()
        # return render(request, 'centerpages/index.html', locals())

    Unaccomplished = 0
    if request.user.telephone == '暂无信息' or request.user.telephone == '':
        Unaccomplished += 1
    if request.user.name == '匿名用户' or request.user.name == '':
        Unaccomplished += 1
    if request.user.introduce == '暂无介绍' or request.user.introduce == '':
        Unaccomplished += 1
    if request.user.address == '暂无信息' or request.user.address == '':
        Unaccomplished += 1
    accomplished = 6 - Unaccomplished

    return render(request, 'centerpages/index.html', locals())


# 重置密码页面
@login_required(login_url='/login')
def resetView(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # old_password = make_password(old_password, None, 'pbkdf2_sha256')
        if not request.user.check_password(old_password):
            tips = '原密码错误'
            return render(request, 'centerpages/reset-password.html', locals())
        else:
            request.user.password = make_password(new_password, None, 'pbkdf2_sha256')
            request.user.save()
            tips = ''
            right_tips = '密码修改成功!'

    return render(request, 'centerpages/reset-password.html', locals())


# 我的动态页面
@login_required(login_url='/login')
def dynamicView(request, page):
    # 获取时间日期
    time_list = ArticleInfo.objects.filter(user_id=request.user.id).order_by('-id').values_list('created')[:5]

    # 获取所有分类标签
    tag_list = ArticleTag.objects.values_list('tag')[:17]
    # print(tag_list)

    # 获取所有文章内容
    # title_list = ArticleInfo.objects.order_by('-id').values_list('title')
    article_list = ArticleInfo.objects.filter(user_id=request.user.id).order_by('-id').all()
    # 分页
    paginator = Paginator(article_list, 3)
    try:
        pageInfo = paginator.page(page)
        print(pageInfo)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)

    return render(request, 'centerpages/dynamic.html', locals())


# 增加动态
@login_required(login_url='/login')
def dynamicAddView(request):
    if request.method == 'POST':
        new_article = ArticleInfo()
        new_article.user_id = request.user.id
        new_article.title = request.POST.get('title')
        new_article.author = request.POST.get('author')
        new_article.content = request.POST.get('gcontent')
        new_article.articlephoto = request.FILES.get('article_image')

        tag = request.POST.get('dropdown')
        new_article.article_tag = ArticleTag.objects.filter(tag=tag)[0]

        new_article.save()
        return redirect('/center/center_dynamic/1')

    # 获取时间日期
    time_list = ArticleInfo.objects.filter(user_id=request.user.id).order_by('-id').values_list('created')[:5]

    # 获取所有分类标签
    tag_list = ArticleTag.objects.values_list('tag')[:17]
    # print(tag_list)
    return render(request, 'centerpages/dynamic-add.html', locals())


# 动态详情
@login_required(login_url='/login')
def dynamicItemView(request, id):
    article = ArticleInfo.objects.get(id=id)

    # 获取时间日期
    time_list = ArticleInfo.objects.filter(user_id=request.user.id).order_by('-id').values_list('created')[:5]

    # 获取所有分类标签
    tag_list = ArticleTag.objects.values_list('tag')[:17]
    # print(tag_list)

    return render(request, 'centerpages/dynamic-item.html', locals())


# 修改动态
@login_required(login_url='/login')
def dynamicEditView(request, id):
    if request.method == 'POST':
        article = ArticleInfo.objects.get(id=id)
        article.user_id = request.user.id
        article.title = request.POST.get('title')
        article.author = request.POST.get('author')
        article.content = request.POST.get('gcontent')
        article.articlephoto = request.FILES.get('article_image')

        tag = request.POST.get('dropdown')
        article.article_tag = ArticleTag.objects.filter(tag=tag)[0]

        article.save()
        return redirect('/center/center_dynamic/1')

    article = ArticleInfo.objects.get(id=id)

    # 获取时间日期
    time_list = ArticleInfo.objects.filter(user_id=request.user.id).order_by('-id').values_list('created')[:5]

    # 获取所有分类标签
    tag_list = ArticleTag.objects.values_list('tag')[:17]
    # print(tag_list)

    return render(request, 'centerpages/dynamic-editor.html', locals())


# 删除动态
@login_required(login_url='/login')
def dynamicDeleteView(request, id):
    ArticleInfo.objects.get(id=id).delete()
    return redirect('/center/center_dynamic/1')


# 我的收藏页面
@login_required(login_url='/login')
def collectionView(request):
    if request.method == 'POST':
        new_collection = CollectionInfo()
        new_collection.image_name = request.POST.get('name')
        new_collection.category = request.POST.get('dropdown')
        new_collection.image = request.FILES.get('image')
        new_collection.description = request.POST.get('description')
        new_collection.user_id = request.user.id

        new_collection.save()

    image_list = CollectionInfo.objects.filter(user_id=request.user.id).order_by('-id').all()[:20]
    return render(request, 'centerpages/collection.html', locals())


# 删除收藏图片
@login_required(login_url='/login')
def collectionDeleteView(request, id):
    CollectionInfo.objects.get(id=id).delete()
    image_list = CollectionInfo.objects.filter(user_id=request.user.id).order_by('-id').all()[:20]
    # return render(request, 'centerpages/collection.html', locals())
    return redirect(reverse('center_collection'))


# 帮助页面
@login_required(login_url='/login')
def helpView(request):
    return render(request, 'centerpages/help.html', locals())


# faq页面
@login_required(login_url='/login')
def faqView(request):
    return render(request, 'centerpages/faq.html', locals())


# 用户画像概览
@login_required(login_url='/login')
def overView(request):
    return render(request, 'centerpages/overview.html', locals())


# 用户画像图表分析
@login_required(login_url='/login')
def analysisView(request):
    return render(request, 'centerpages/analysis.html', locals())


# 生成图表
def graphView(request):
    # 动态文章分类-分类文章数量 折线图
    from matplotlib import pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文

    # 创建第一个画板
    plt.figure(figsize=(12, 4))
    plt.figure(1)

    x1 = []
    tag_list = ArticleTag.objects.all().values_list('tag')
    for tag in tag_list:
        x1.append(tag[0])

    y1 = []
    for i in range(1, 18):
        count = ArticleInfo.objects.filter(user_id=request.user.id, article_tag_id=i).count()
        y1.append(count)
    plt.plot(x1, y1, linestyle='-', color='steelblue', label='分类文章数量')
    print(x1)
    print(y1)

    plt.ylabel("文章数量/篇")
    plt.title("动态文章分类-分类文章数量折线图")
    plt.xticks()
    plt.legend()

    # ========================================================================================
    # 创建第二个画板
    plt.figure(figsize=(12, 4))
    plt.figure(2)

    # 动态文章名称 - 文章长度 柱状图
    x2 = []
    article_list = ArticleInfo.objects.all().values_list('title')
    for article in article_list:
        x2.append(article[0])

    y2 = []
    long_list = ArticleInfo.objects.all().values_list('content')
    for item in long_list:
        y2.append(len(item[0]))

    new_bar = plt.bar(x2, y2, color='steelblue', label='文章字符数', width=0.5)
    plt.xticks()
    plt.ylabel("文章长度/字符")
    plt.title("动态文章名称-文章长度柱状图")
    plt.legend()

    # 添加数据标签
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
            # 柱形图边缘用白色填充，纯粹为了美观
            rect.set_edgecolor('white')
    add_labels(new_bar)

    # ========================================================================================
    # 创建第三个画板
    plt.figure(figsize=(12, 4))
    plt.figure(3)
    # 省市区高校信息图
    names = ('总数量', '已经建立词库的数量')  # 姓名
    areas = ['天津市', '江苏省', '浙江省', '上海市', '北京市', '湖北省']  # 地区

    list1 = []
    for area in areas:
        list1.append(SchoolInfo.objects.filter(area=area).count())

    list2 = []
    for area in areas:
        list2.append(SchoolInfo.objects.filter(area=area, is_build=1).count())
    print(list2)
    # 设置柱形图宽度
    bar_width = 0.3

    index = np.arange(len(list1))
    # 总数量
    rects1 = plt.bar(index, list1, bar_width, color='dodgerblue', label=names[0])
    # 建立词库的数量
    rects2 = plt.bar(index + bar_width, list2, bar_width, color='lightgreen', label=names[1])
    # X轴标题
    plt.xticks(index + 0.15, areas)
    # Y轴范围
    plt.ylim(ymax=30, ymin=0)
    # 图表标题
    plt.title('全国各省市区高校信息图')
    plt.ylabel("高校数量/所")
    plt.legend()
    # 添加数据标签
    def add_labels(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2, height, height, ha='center', va='bottom')
            # 柱形图边缘用白色填充，纯粹为了美观
            rect.set_edgecolor('white')
    add_labels(rects1)
    add_labels(rects2)

    # ========================================================================
    # 创建第四个画板
    plt.figure(figsize=(12, 4))
    plt.figure(4)
    x4 = []
    y4 = []
    schoolName_list = SchoolInfo.objects.all().filter(is_build=1).values_list('school_name')
    for school in schoolName_list:
        x4.append(school[0])
        id = SchoolInfo.objects.get(school_name=school[0]).id
        y4.append(CntToUrl.objects.filter(school_id=id).count())


    plt.plot(x4, y4, linestyle='-', color='steelblue', label='词库数量')
    plt.xticks()
    plt.ylabel("词库数量/个")
    plt.title("已建立词库高校-词库数量折线图")
    plt.xticks(rotation=-45)
    plt.legend()

    # 调整每隔子图之间的距离
    plt.tight_layout()
    plt.figure(1).savefig('publicStatic/assets/images/centergraph1.png', dpi=97)
    plt.figure(2).savefig('publicStatic/assets/images/centergraph2.png', dpi=98)
    plt.figure(3).savefig('publicStatic/assets/images/searchgraph1.png', dpi=99)
    plt.figure(4).savefig('publicStatic/assets/images/searchgraph2.png', dpi=100)

    return redirect(reverse('center_analysis'))

