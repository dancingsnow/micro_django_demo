from django.db import models


# Create your models here.

class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    # 与AuthorDetail建立一对一的关系
    author_detail = models.OneToOneField(to="AuthorDetail", on_delete=models.CASCADE)

    def __str__(self):
        return "(%s, %s)"%(self.nid, self.name)

    class Meta:
        db_table = "author"
        verbose_name = "作者"
        verbose_name_plural = "作者们"



class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday = models.DateField()
    telephone = models.CharField(max_length=16)
    addr = models.CharField(max_length=64)

    def __str__(self):
        return "(%s, %s)"%(self.nid, self.birthday)

    class Meta:
        db_table = "author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = "作者们详情"


class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    email = models.EmailField()

    class Meta:
        db_table = "publish"


class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 与Publish建立一对多的关系,外键字段建立在多的一方
    publish = models.ForeignKey(to="Publish", to_field="nid", on_delete=models.CASCADE)
    # 与Author表建立多对多的关系,ManyToManyField可以建在两个模型中的任意一个，自动创建第三张表
    authors = models.ManyToManyField(to='Author', )

    class Meta:
        db_table = "book"
