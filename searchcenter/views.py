import math

import chardet
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import jieba
import re
from collections import deque
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


# 搜索主页
from django.urls import reverse

from searchcenter.models import SchoolInfo, CntToUrl, WordToCnt, SearchResult, SearchHistory, Category


@login_required(login_url='/login')
def indexView(request):
    build_school_list = SchoolInfo.objects.filter(is_build="1")
    build_count = SchoolInfo.objects.filter(is_build="1").count()
    total_count = SchoolInfo.objects.all().count()
    unbuild_count = int(total_count) - int(build_count)

    all_school_id_str = ""
    for school in build_school_list:
        all_school_id_str = all_school_id_str + str(school.id) + " "

    return render(request, 'searchpages/index.html', locals())


# 词库管理
@login_required(login_url='/login')
def manageView(request, page):
    if request.method == 'POST':
        id = request.POST.get('school_id')
        edit_school = SchoolInfo.objects.get(id=id)
        edit_school.school_name = request.POST.get('school_name')
        edit_school.school_url = request.POST.get('school_url')
        edit_school.area = request.POST.get('dropdown')
        edit_school.detail = request.POST.get('description')
        edit_school.save()
    build_school_list = SchoolInfo.objects.filter(is_build="1")
    paginator = Paginator(build_school_list, 5)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    strat = (page - 1) * 5
    return render(request, 'searchpages/lib-manage.html', locals())


# 词库管理中的删除
@login_required(login_url='/login')
def manageDelView(request, id):
    school = SchoolInfo.objects.get(id=id)
    school.is_build = 0
    school.save()

    CntToUrl.objects.filter(school_id=id).delete()
    WordToCnt.objects.filter(school_id=id).delete()

    return redirect('/search/search_manage/1')


# # 词库管理中的编辑
# @login_required(login_url='/login')
# def manageEditView(request):
#     return HttpResponse('asjdhsf')


# 学校列表
@login_required(login_url='/login')
def schoolListView(request):
    school_list = SchoolInfo.objects.filter(user_id=request.user.id).all()
    return render(request, 'searchpages/school-list.html', locals())


# 分类检索和相关推荐
@login_required(login_url='/login')
def recommendView(request):
    build_school_list = SchoolInfo.objects.filter(is_build="1")
    all_school_id_str = ""
    for school in build_school_list:
        all_school_id_str = all_school_id_str + str(school.id) + " "
    return render(request, 'searchpages/category.html', locals())


# 搜索帮助
@login_required(login_url='/login')
def helpView(request):
    return render(request, 'searchpages/search-help.html', locals())


# 建立词库
@login_required(login_url='/login')
def buildView(request, id):
    # 标记为已经建立
    school = SchoolInfo.objects.get(id=id)
    school.is_build = 1
    school.save()

    print('*********************************开始爬取数据******************************************')
    url = SchoolInfo.objects.get(id=id).school_url
    # 数据库对应操作

    # get_info API
    count = 0
    # BFS所需的队列
    my_queue = deque()
    # set集合存储已经访问过的链接
    used_list = set()
    used_list2 = set()
    # 首页入队
    my_queue.append(url)
    while my_queue:
        if count >= 10:
            break
        # 每次都从队列中移除第一个元素
        url = my_queue.popleft()
        # 放入已访问的集合中
        used_list.add(url)
        used_list2.add(url)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE/10.0.2071.0 '
            }
            response = requests.get(url, headers=headers, timeout=3)
            # 避免中文乱码
            response.encoding = response.apparent_encoding
            content = response.text
        # 不能访问的网页，则跳过进行下一轮循环
        except requests.exceptions.RequestException:
            print('该网页无法正常访问：' + url)
            continue
        # 匹配网页中的URL
        pattern = re.compile('<a.*?(http://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|])', re.S)
        m = re.findall(pattern, content)
        m1 = []
        for item in m:
            if (item not in m1) and (item + '/' not in m1) and (item[:-1] not in m1) \
                    and (item not in used_list2) and (item + '/' not in used_list2) and (item[:-1] not in used_list2):
                used_list2.add(item)
                m1.append(item)
        # 学校的内网应该有‘tust’关键词，这里为了减少网页数量，增加了一些限制条件，这里把(x.endswith('cn')删除即可统计所有文件
        for x in m1:
            if (x not in used_list) and (x + '/' not in used_list) and (x[:-1] not in used_list):
                if (x.endswith('cn')) or (x.endswith('html')) or (x.endswith('htm')) or (x.endswith('cn/')) or (
                        x.endswith('html/')) or (x.endswith('htm/')):
                    my_queue.append(x)
        # 制定解析方式
        soup = BeautifulSoup(content, 'html.parser')
        # 文档标题
        title = soup.title
        true_title = ""
        if title:
            true_title = title.text

        # 文档内容
        article = soup.getText()
        # case1:无标题无内容，直接下一轮循环
        if title is None and article is None:
            continue
        # case2：有标题，无内容，此时需要把内容置空
        elif article is None and title is not None:
            title = title.text
            article = ''
        # case3：有内容，无标题，此时需要把标题置空
        elif title is None and article is not None:
            title = ''
        # case4:有标题有内容
        else:
            title = title.text*10
        # 进行分词，讲标题和内容的分词结果放入sep_list中
        sep_list = list(jieba.cut_for_search(title))
        sep_article = jieba.cut_for_search(article)
        sep_list += list(sep_article)

        # 放入第一张数据表，即网页所对应的URL，方便查询的时候取出URL
        # sql = 'insert into searchcenter_cnttourl(cnt, url, title, school_id) values(count, url, title, 1)'
        # data = (count, url, title, 1)
        # cursor.execute(sql % data)
        count += 1
        print('成功爬取第', count, '个网页：', url)

        cnt_to_url = CntToUrl()

        cnt_to_url.school_id = id
        cnt_to_url.cnt = count
        cnt_to_url.title = true_title
        cnt_to_url.url = url
        cnt_to_url.save()

        # 下面的for循环是为了构建第二张数据表，字段为每个分词，字段的值为出现该词的网页ID号，若重复，则在后面追加，方便统计次数
        for word in sep_list:
            result = WordToCnt.objects.filter(school_id=id, word=word)
            if len(result) == 0:
                doc_list_str = str(count)
                word_to_cnt = WordToCnt()
                word_to_cnt.school_id = id
                word_to_cnt.word = word
                word_to_cnt.cnt_list = doc_list_str
                word_to_cnt.save()
                # cursor.execute('insert into word_to_cnt values(?,?)', (word, doc_list_str))
            else:
                doc_list_str = result[0].cnt_list
                doc_list_str += ' ' + str(count)
                result[0].cnt_list = doc_list_str
                result[0].save()
                # cursor.execute('update word_to_cnt set list=? where word=?', (doc_list_str, word))

    print('*********************************该网页词表建立完毕*************************************')

    return redirect(reverse('search_schoolList'))


# 搜索结果
@login_required(login_url='/login')
def searchResultView(request, schoolStr, keywords, page):
    # 获得需要查询的学校列表
    school_list = schoolStr.split(" ")[:-1]
    # 获得查询关键词列表
    sep_search_word = jieba.cut_for_search(keywords)
    keywords_list = []
    for word in sep_search_word:
        keywords_list.append(word)
    # 清空结果表
    SearchResult.objects.all().delete()

    for school in school_list:
        # 获取文档总数，该值为计算IDF值所必需
        web_count = CntToUrl.objects.filter(school_id=school).count()
        # 结果字典：{文档号：文档TF-IDF值}
        score = {}
        for word in keywords_list:
            if word == ' ':
                continue
            # {文档号：文档中出现该单词的次数}
            doc_count = {}
            # 根据关键词查询文档列表
            # cursor.execute('select list from word_to_cnt where word=?', (word,))
            # result = cursor.fetchall()
            result = WordToCnt.objects.filter(school_id=int(school), word=word)

            if len(result) > 0:
                doc_list_str = result[0].cnt_list
                doc_list_str = doc_list_str.split(' ')
                # 把字符串转换为int类型的列表
                doc_list_str = [int(x) for x in doc_list_str]
                # set集合具有不重复的特性，可以方便的统计该查询词在多少个文档中出现

                idf_len = len(set(doc_list_str))

                if idf_len == 0:
                    idf_len = idf_len + 1
                else:
                    if web_count == idf_len:
                        web_count = web_count + 1

                # IDF值的计算公式
                idf = math.log(web_count / idf_len)

                # 计算文档中出现查询词的次数
                for num in doc_list_str:
                    if num in doc_count:
                        doc_count[num] = doc_count[num] + 1
                    else:
                        doc_count[num] = 1
                # 计算TF-IDF值，公式为TF*IDF
                for num in doc_count:
                    if num in score:
                        # 该类情况一般不会出现，因为前面的文档列表在获取时已经进行了去重，所以doc_count的键都是不重复的
                        score[num] = score[num] + doc_count[num] * idf
                    else:
                        score[num] = doc_count[num] * idf
        # 降序排序
        sorted_list = sorted(score.items(), key=lambda d: d[1], reverse=True)
        print(sorted_list)
        # print("------------------------")
        # for elem in sorted_list:
        #     all_sorted_list.append(elem)
        # print(all_sorted_list)

        # 结果函数
        cnt = 0
        # all_sorted_list = sorted(score.items(), key=lambda d: d[1], reverse=True)
        for num, doc_score in sorted_list:
            cnt = cnt + 1
            # cursor.execute('select link from cnt_to_url where id=?', (num,))
            # 获取页面的网址
            # url = cursor.fetchall()[0][0]
            # print('------------------------------------')
            # print(CntToUrl.objects.filter(school_id=school, cnt=num).values('url'))
            # print('------------------------------------')
            url = CntToUrl.objects.filter(school_id=school, cnt=num).values('url')[0]

            title = CntToUrl.objects.filter(school_id=school, cnt=num).values('title')[0]
            search_res = SearchResult()
            if title['title'] is None or title['title'] == '':
                search_res.title = '无标题'
                print('无标题')
            else:
                print(str(cnt) + ':' + title['title'])
                search_res.title = title['title']

            search_res.url = url['url']
            search_res.tf_idf = doc_score
            search_res.save()

            print(url['url'], '\t\tTF—IDF：', doc_score)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        if cnt == 0:
            print('该关键词无搜索结果')

    result_list = SearchResult.objects.all().order_by('-tf_idf')
    input_keyword = keywords
    input_schoolStr = schoolStr

    paginator = Paginator(result_list, 5)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    strat = (page - 1) * 5

    # 历史记录
    history_byTime = SearchHistory.objects.order_by('-updated').all()[:6]
    history_byCount = SearchHistory.objects.order_by('-count').all()[:8]
    return render(request, 'searchpages/search-result.html', locals())


# 分类搜索结果
@login_required(login_url='/login')
def categoryResultView(request, schoolStr, keywords, page):
    # 获得需要查询的学校列表
    school_list = schoolStr.split(" ")[:-1]
    # 获得查询关键词列表
    print(keywords)
    sep_search_word_list = Category.objects.get(category_name=keywords).category_list
    sep_search_word = jieba.cut_for_search(sep_search_word_list)
    keywords_list = []
    for word in sep_search_word:
        keywords_list.append(word)
    # 清空结果表
    SearchResult.objects.all().delete()

    for school in school_list:
        # 获取文档总数，该值为计算IDF值所必需
        web_count = CntToUrl.objects.filter(school_id=school).count()
        # 结果字典：{文档号：文档TF-IDF值}
        score = {}
        for word in keywords_list:
            if word == ' ':
                continue
            # {文档号：文档中出现该单词的次数}
            doc_count = {}
            # 根据关键词查询文档列表
            # cursor.execute('select list from word_to_cnt where word=?', (word,))
            # result = cursor.fetchall()
            result = WordToCnt.objects.filter(school_id=int(school), word=word)

            if len(result) > 0:
                doc_list_str = result[0].cnt_list
                doc_list_str = doc_list_str.split(' ')
                # 把字符串转换为int类型的列表
                doc_list_str = [int(x) for x in doc_list_str]
                # set集合具有不重复的特性，可以方便的统计该查询词在多少个文档中出现
                idf_len = len(set(doc_list_str))

                if idf_len == 0:
                    idf_len = idf_len + 1
                else:
                    if web_count == idf_len:
                        web_count = web_count + 1

                # IDF值的计算公式
                idf = math.log(web_count / idf_len)

                # 计算文档中出现查询词的次数
                for num in doc_list_str:
                    if num in doc_count:
                        doc_count[num] = doc_count[num] + 1
                    else:
                        doc_count[num] = 1
                # 计算TF-IDF值，公式为TF*IDF
                for num in doc_count:
                    if num in score:
                        # 该类情况一般不会出现，因为前面的文档列表在获取时已经进行了去重，所以doc_count的键都是不重复的
                        score[num] = score[num] + doc_count[num] * idf
                    else:
                        score[num] = doc_count[num] * idf
        # 降序排序
        sorted_list = sorted(score.items(), key=lambda d: d[1], reverse=True)
        print(sorted_list)
        # print("------------------------")
        # for elem in sorted_list:
        #     all_sorted_list.append(elem)
        # print(all_sorted_list)

        # 结果函数
        cnt = 0
        # all_sorted_list = sorted(score.items(), key=lambda d: d[1], reverse=True)
        for num, doc_score in sorted_list:
            cnt = cnt + 1
            # cursor.execute('select link from cnt_to_url where id=?', (num,))
            # 获取页面的网址
            # url = cursor.fetchall()[0][0]
            url = CntToUrl.objects.filter(school_id=school, cnt=num).values('url')[0]
            title = CntToUrl.objects.filter(school_id=school, cnt=num).values('title')[0]
            search_res = SearchResult()
            if title['title'] is None or title['title'] == '':
                search_res.title = '无标题'
                print('无标题')
            else:
                print(str(cnt) + ':' + title['title'])
                search_res.title = title['title']

            search_res.url = url['url']
            search_res.tf_idf = doc_score
            search_res.save()

            print(url['url'], '\t\tTF—IDF：', doc_score)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        if cnt == 0:
            print('该关键词无搜索结果')

    result_list = SearchResult.objects.all().order_by('-tf_idf')
    input_keyword = keywords
    input_schoolStr = schoolStr

    paginator = Paginator(result_list, 5)
    try:
        pageInfo = paginator.page(page)
    except PageNotAnInteger:
        pageInfo = paginator.page(1)
    except EmptyPage:
        pageInfo = paginator.page(paginator.num_pages)
    strat = (page - 1) * 5
    return render(request, 'searchpages/category-result.html', locals())


# 历史记录
@login_required(login_url='/login')
def historyView(request):
    id = request.GET.get('id')
    res = SearchResult.objects.get(id=id)
    print(res)
    # 创建一个历史记录对象
    is_exist = SearchHistory.objects.filter(url=res.url)
    if is_exist.exists():
        exist = SearchHistory.objects.get(url=res.url)
        exist.count = exist.count + 1
        exist.save()
    else:
        history = SearchHistory()
        history.url = res.url
        history.title = res.title
        history.count = 1
        history.save()
