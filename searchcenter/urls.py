from django.urls import path, include
from .views import *
urlpatterns = [
    path('search_index', indexView, name='search_index'),
    path('search_manage/<int:page>', manageView, name='search_manage'),
    path('search_manageDelete/<int:id>', manageDelView, name='search_manageDelete'),
    # path('search_manageEdit', manageEditView, name='search_manageEdit'),
    path('search_schoolList', schoolListView, name='search_schoolList'),
    path('search_recommend', recommendView, name='search_recommend'),
    path('search_help', helpView, name='search_help'),
    path('search_build/<int:id>', buildView, name='search_build'),
    path('search_searchResult/<schoolStr>/<keywords>/<int:page>', searchResultView, name='search_searchResult'),
    path('search_categoryResult/<schoolStr>/<keywords>/<int:page>', categoryResultView, name='search_categoryResult'),
    path('search_history', historyView, name='search_history')
]
