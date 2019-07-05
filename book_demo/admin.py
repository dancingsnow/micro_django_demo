from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django import forms
from book_demo.models import *

class AuthorForm(forms.Form):
    name = forms.CharField(error_messages={'required':'用户名不能为空'})
    age = forms.CharField(error_messages={'required':'年龄不能为空'})
    class Meta:
        model = Author
        fields = '__all__'

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['nid','name', 'age']
    search_fields = ['nid', 'name', 'age']
    list_filter = ['nid', 'name', 'age']

# 方式一
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publish)
admin.site.register(Book)


# 方式二
@admin.register(AuthorDetail)
class AuthorDetailAdmin(admin.ModelAdmin):
    list_display = ['nid', 'birthday', 'telephone', 'addr']