from django.contrib import admin

from .models import Directory
from .models import File, FileSection, SectionCategory, Status, StatusData
from .models import User


admin.site.register(Directory)
admin.site.register(File)
admin.site.register(FileSection)
admin.site.register(SectionCategory)
admin.site.register(Status)
admin.site.register(StatusData)
