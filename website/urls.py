from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from rest_framework.documentation import include_docs_urls

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from apps.article.views import ArticleCreated
from apps.course.views import CoursesList, CourseCreatedList, CourseListCreated, MeCoursesList
from apps.dynamic .views import Home
from apps.forum.views import Forum_templateView, ForumView, CommentView, Parent_CommentView, ForumListView
from apps.support.views import LinkList, EmailsList, BannerList, QQList, SeoList
from apps.user.views import test, captcha_refresh, verify, login_view, UserGetInfo, UserGetAllInfo, \
    PersonOthers, Register, active_user, get_message, UserMessages, qq, getClback, getClbackQQ, UserFollows, AppMessage, \
    UserFollowOther
from django.views.generic import TemplateView

from website import settings
from apps.article import views
from apps.user.views import logout_view, Person, PersonApi,to_login
from rest_framework import routers

router = routers.DefaultRouter()
router.register('article_list', views.ArticleListView)
router.register('me_article_list', views.MeArticleListView)
router.register('ArticleCommit', views.ArticleCommit)
router.register('follow_list', views.FollowListView)
router.register('category', views.CategoryView)
router.register('Article_Comment', views.ArticleCommentView)
router.register('comment_reply', views.ArticleCommentReplyView)
router.register('PersonApi', PersonApi)
router.register('apiinfo', UserGetInfo)
router.register('all_info', UserGetAllInfo)
# router.register('user_disbale', UserDisbale)
router.register('PersonOthers', PersonOthers)
router.register('UserMessages', UserMessages, basename='UserMessages')
router.register('article', ArticleCreated)
router.register('courseList', CoursesList)
router.register('mecourseList', MeCoursesList)
router.register('course', CourseCreatedList)
router.register('Addtutorial', CourseListCreated)
router.register('BannerList', BannerList)
router.register('EmailsList', EmailsList)
router.register('LinkList', LinkList)
router.register('forum/category', Forum_templateView)
router.register('forum', ForumView)
router.register('CommentView', CommentView)
router.register('Parent_CommentView', Parent_CommentView)
router.register('get-list',QQList)
router.register('seo-list',SeoList,basename='seo-list')
router.register('UserFollows',UserFollows)
router.register('AppMessage',AppMessage)
router.register('UserFollowOther',UserFollowOther)
router.register('ForumListView',ForumListView)

urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    path('refresh/', captcha_refresh),  # 这是生成验证码的图片
    path('verify/', verify),  # 这是生成验证码的图片
    path('', views.Home, name='home'),

    path('webapp/', TemplateView.as_view(template_name='webapp/index.html')),
    path('login/', login_view, name='index'),
    path('info/', get_message, name='info'),
    path('person/', include('apps.user.urls')),
    path('logout/', logout_view, name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('article/', include('apps.article.urls')),
    path('course/', include('apps.course.urls')),
    path('support/', include('apps.support.urls')),
    path('forum/', include('apps.forum.urls')),
    path('ads.txt/',TemplateView.as_view(template_name='ads.txt')),
    path('root.txt/', TemplateView.as_view(template_name='root.txt')),
    path('jd_root.txt/', TemplateView.as_view(template_name='jd_root.txt')),
    path('gome_20943.txt/', TemplateView.as_view(template_name='gome_20943.txt')),
    #url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', active_user, name='active_user'),
    path('activate/<str:token>', active_user, name='active_user'),
    url(r'^search/', include('haystack.urls'), name='haystack_search'),

    url(r'^upload/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url("api-docs/", include_docs_urls("API文档")),
    url(r'api/login/$', obtain_jwt_token),  # jwt认证
    url(r'^api-token-refresh/', refresh_jwt_token),#jwt刷新
    path('auth-qq', to_login, name='qq-login'),
    path('qq', qq, name='qq'),
    path('callbackget', getClback, name='callbackget'),
    path('getClbackQQ', getClbackQQ, name='getClbackQQ'),
    url(r'^static/(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
]

#全局404
handler404='apps.user.views.page_not_found'
handler500='apps.user.views.page_error'