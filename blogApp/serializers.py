from rest_framework import serializers

from .models import *


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        # fields = ['id','first_name','last_name','age','email','phone','address']
        # exclude = ['id']
        fields = "__all__"
