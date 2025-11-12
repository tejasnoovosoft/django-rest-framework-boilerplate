from django.db import models


class Category(models.Model):
    class Meta:
        db_table = "blog_categories"

    name = models.CharField(max_length=100, unique=True)
