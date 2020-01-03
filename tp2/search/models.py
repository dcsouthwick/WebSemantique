from django.db import models

# Create your models here.

class Query(models.Model):
    query = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = "queries"
    def __str__(self):
        return self.query 