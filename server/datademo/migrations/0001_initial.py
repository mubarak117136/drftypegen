# Generated by Django 3.0.3 on 2020-02-06 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
            ],
            options={
                'verbose_name': 'book',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(verbose_name='bio')),
                ('birthday', models.DateField(verbose_name='Birthday')),
                ('deathday', models.DateField(blank=True, null=True, verbose_name='Deathday')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Person_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Person',
            },
        ),
        migrations.CreateModel(
            name='PersonBookRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datademo.Book', verbose_name='')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datademo.Person')),
            ],
            options={
                'verbose_name': 'Personbookrelation',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='contributors',
            field=models.ManyToManyField(related_name='books', through='datademo.PersonBookRelation', to='datademo.Person', verbose_name='Contributors'),
        ),
    ]
