from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import Account

@admin.register(Account)
class AccoubtAdmin(ImportExportModelAdmin):
    def get_export_filename(self, file_format):
        filename = "%s.%s" % ("your_custom_filename",
                             file_format.get_extension())
        return filename
    pass