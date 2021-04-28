from rest_framework import serializers

from apps.course.models import Courses, CourseList
from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','avatar','id')


class AddtutorialSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = CourseList
        fields ='__all__'


class CourseSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    image = serializers.ImageField(required=False)
    user = UserSerializer(read_only=True)
    courselist_set = AddtutorialSerializers(many=True)
    class Meta:
        model = Courses
        fields = '__all__'



class CreatedCourseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = '__all__'




