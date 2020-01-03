from django.contrib import admin

# Register your models here.
from .models import Query
class QueryAdmin(admin.ModelAdmin):
    display=("query")
admin.site.register(Query, QueryAdmin)