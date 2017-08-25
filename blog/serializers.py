from django.contrib.auth.models import User, Permission
from rest_framework import serializers

from blog.models import Post


class CustomModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class CustomHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomHyperlinkedModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class PostSerializer(CustomModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(CustomHyperlinkedModelSerializer):
    post_set = serializers.HyperlinkedRelatedField(many=True, view_name='blog:post-detail', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="blog:user-detail")

    class Meta:
        model = User
        fields = ('id', 'post_set', 'url')
        # exclude = ('password', )
        # fields = '__all__'

