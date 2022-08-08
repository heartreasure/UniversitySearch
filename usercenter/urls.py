from django.urls import path, include
from .views import *
urlpatterns = [
    # 我的动态URL
    path('center_index', indexView, name='center_index'),
    path('center_resetPassword', resetView, name='center_resetPassword'),
    path('center_dynamic/<int:page>', dynamicView, name='center_dynamic'),
    path('center_help', helpView, name='center_help'),
    path('center_faq', faqView, name='center_faq'),
    path('center_dynamicAdd', dynamicAddView, name='center_dynamicAdd'),
    path('center_dynamicItem/<int:id>', dynamicItemView, name='center_dynamicItem'),
    path('center_dynamicEdit/<int:id>', dynamicEditView, name='center_dynamicEdit'),
    path('center_dynamicDelete/<int:id>', dynamicDeleteView, name='center_dynamicDelete'),
    # 我的收藏URL
    path('center_collection', collectionView, name='center_collection'),
    path('center_collectionDelete/<int:id>', collectionDeleteView, name='center_collectionDelete'),
    # 我的用户画像
    path('center_overview', overView, name='center_overview'),
    path('center_analysis', analysisView, name='center_analysis'),
    # 生成图表
    path('center_graph', graphView, name='center_graph'),
]
