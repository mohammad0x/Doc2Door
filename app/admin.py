from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(News)
class reseveAdmin(admin.ModelAdmin):
    list_filter = ['accept' , 'created_at']
admin.site.register(Reserve ,reseveAdmin )
admin.site.register(Category)

