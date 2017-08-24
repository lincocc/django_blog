from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Post


class CustomModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class PostSerializer(CustomModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = '__all__'
        extra_fields = ['user']


class UserSerializer(CustomModelSerializer):
    post_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        exclude = ('password',)
        extra_fields = ['post_set']
