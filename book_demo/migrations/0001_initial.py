# Generated by Django 2.2.3 on 2019-07-09 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('age', models.IntegerField()),
            ],
            options={
                'verbose_name': '作者',
                'verbose_name_plural': '作者们',
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='AuthorDetail',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('birthday', models.DateField()),
                ('telephone', models.CharField(max_length=16)),
                ('addr', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': '作者详情',
                'verbose_name_plural': '作者们详情',
                'db_table': 'author_detail',
            },
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'publish',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32)),
                ('publishDate', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('authors', models.ManyToManyField(to='book_demo.Author')),
                ('publish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_demo.Publish')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.AddField(
            model_name='author',
            name='author_detail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='book_demo.AuthorDetail'),
        ),
    ]
