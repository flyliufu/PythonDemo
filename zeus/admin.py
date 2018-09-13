from django.contrib import admin
from zeus.bean.Menu import Menu

admin.site.title = "微信管理系统"
admin.site.site_title = "微信管理系统"
admin.site.site_header = "微信管理系统"
admin.site.register(Menu)
