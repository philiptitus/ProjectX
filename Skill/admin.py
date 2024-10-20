from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Skill)
admin.site.register(Trade)
admin.site.register(Review)
admin.site.register(Queue)
admin.site.register(Message)