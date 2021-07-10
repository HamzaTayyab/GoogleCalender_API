from django.contrib import admin
from googleapi.models import teachers
from django.shortcuts import redirect
from googleapi.views import modelCreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
# Register your models here.


admin.site.site_header = "JakStat Tutors"
admin.site.site_title = "JakStat Tutors"
admin.site.index_title = " "


@admin.register(teachers)
class teacherAdmin(admin.ModelAdmin):
    # form = CustomFooForm
    list_display = [
        "name",
        "email",
        "calculations",
        "clinical_pharmacy",
        "pharmacy_law",
        "compounding_exam",
        "general_pharmacology",
        "imagelink"
    ]
    fields = (
        "name",
        "email",
        "calculations",
        "clinical_pharmacy",
        "pharmacy_law",
        "compounding_exam",
        "general_pharmacology",
        "imagelink",

    )
    list_filter = [
        "calculations",
        "clinical_pharmacy",
        "pharmacy_law",
        "compounding_exam",
        "general_pharmacology"
    ]
    search_fields = (
        "name",
        "email",
    )

    def save_model(self, request, obj, form, change):
        super(teacherAdmin, self).save_model(request, obj, form, change)
        # return redirect('http://127.0.0.1:8000/ext')

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/ext/'+str(obj.id), id=obj.id)
