import json

from django.core.paginator import PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,HttpResponse
# Create your views here.
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from pure_pagination import Paginator
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.article.views import StandardResultsSetPagination
from apps.course.filter import CoursesFilter
from apps.course.models import Courses, CourseList
from apps.course.serializers import CourseSerializers, CreatedCourseSerializers, AddtutorialSerializers
from apps.support.models import Seo
from apps.uitls.jsonserializable import DateEncoder
from apps.uitls.permissions import IsOwnerOrReadOnly, IsOwnerOrRead


def List(request):
    """TODO 教程列表  标签根据uuid Detail视图渲染对应的所有文章"""
    course = Courses.objects.all()
    #seo_list =get_object_or_404(Seo,name='教程')
    return render(request,'pc/course/index.html',{'course':course})


def Detail(request,course_id,list_id):
    """TODO 文章视图 根据uuid来查询对应所有文章
    """
    course_list = CourseList.objects.filter(course=course_id)
    content = get_object_or_404(course_list, pk=list_id)
    previous_blog = course_list.filter(id__lt=list_id).last()
    next_blog = course_list.filter(id__gt=list_id).first()
    return render(request,'pc/course/detail.html',{'course':course_list,'uuid':course_id,'content':content,'previous_blog':previous_blog,'next_blog':next_blog})


def courseViewApi(request,courses_id):
    course = Courses.objects.get(pk=courses_id)
    course_list = course.courselist_set.all()
    try:
        page = request.GET.get('page', 1)
        if page == '':
            page = 1
    except PageNotAnInteger:
        page = 1

    p = Paginator(course_list,10,request=request)
    people = p.page(page)
    print(people.object_list)
    print(people.next_page_number)
    return HttpResponse()


class CoursesList(viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CourseSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination


class MeCoursesList(viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CourseSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Courses.objects.filter(user=self.request.user)

class CourseCreatedList(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = Courses.objects.filter(is_delete=False)
    serializer_class = CreatedCourseSerializers
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]
    filter_backends = (DjangoFilterBackend,)
    filter_class = CoursesFilter


class CourseListCreated(mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.ReadOnlyModelViewSet):
    queryset = CourseList.objects.all()
    serializer_class = AddtutorialSerializers
    permission_classes = (IsAuthenticated, IsOwnerOrRead)  # 未登录禁止访问
    authentication_classes = [JSONWebTokenAuthentication]

