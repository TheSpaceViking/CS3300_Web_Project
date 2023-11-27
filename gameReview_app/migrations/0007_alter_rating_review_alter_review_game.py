# Generated by Django 4.2.7 on 2023-11-26 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameReview_app', '0006_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='review',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_ratings', to='gameReview_app.review'),
        ),
        migrations.AlterField(
            model_name='review',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gameReview_app.game'),
        ),
    ]
