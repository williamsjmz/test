# Generated by Django 4.0.3 on 2022-03-21 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portales', '0007_alter_page_design'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='design',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='portales.design'),
            preserve_default=False,
        ),
    ]