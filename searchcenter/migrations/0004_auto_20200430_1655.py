# Generated by Django 2.2.12 on 2020-04-30 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchcenter', '0003_schoolinfo_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=100, verbose_name='网址')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('tf_idf', models.CharField(max_length=200, verbose_name='TF-IDF')),
            ],
        ),
        migrations.AlterField(
            model_name='cnttourl',
            name='url',
            field=models.CharField(max_length=100, verbose_name='子网页URL'),
        ),
    ]