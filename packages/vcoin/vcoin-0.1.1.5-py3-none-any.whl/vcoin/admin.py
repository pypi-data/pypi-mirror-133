from django.contrib import admin

# Register your models here.
from vcoin.models import VCoinModel, VCoinConfigModel, VCoinHistory

admin.site.register(VCoinModel)
admin.site.register(VCoinConfigModel)
admin.site.register(VCoinHistory)
