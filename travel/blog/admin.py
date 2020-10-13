from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib import messages
from django.utils.translation import ngettext
from django.http import HttpResponse
import xlwt
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.


@admin.register(Banner)
class AdminBanner(admin.ModelAdmin):
    list_display = ['title', 'status', 'show_image']
    search_fields = ['title', 'status']

    class Meta:
        verbose_name_plural = 'Banner'

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Images'


@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['contact', 'email', 'location', 'status', 'show_image']
    search_fields = ['contact', 'email', 'location', 'status']

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.logo.url))

    show_image.short_description = 'Logo'


@admin.register(Destination)
class AdminDestination(admin.ModelAdmin):
    list_per_page = 20
    ordering = ['category']
    hierarchy = 'category'
    list_filter = ['category']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'status', 'popular', 'category', 'show_image']
    search_fields = ['title', 'status', 'popular']
    actions = ['update_popular_active', 'update_popular_inactive', 'update_status_active', 'update_status_inactive']

    def update_popular_active(self, request, queryset):
        updated = queryset.update(popular=True)
        self.message_user(request, ngettext(
            '%d Destination Package will be shown on Home Page at Popular Package Section',
            '%d Destinations Package will be shown on Home Page at Popular Package Section',
            updated,
        ) % updated, messages.SUCCESS)

    update_popular_active.short_description = 'Popular'

    def update_popular_inactive(self, request, queryset):
        updated = queryset.update(popular=False)
        self.message_user(request, ngettext(
            '%d Destination Package will be removed from Home Page at Popular Package Section',
            '%d Destinations Package will be removed from Home Page at Popular Package Section',
            updated,
        ) % updated, messages.SUCCESS)

    update_popular_inactive.short_description = 'Not Popular'

    def update_status_active(self, request, queryset):
        queryset.update(status=True)

    update_status_active.short_description = 'Active'

    def update_status_inactive(self, request, queryset):
        queryset.update(status=False)

    update_status_inactive.short_description = 'Inactive'

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Image'


@admin.register(Destination_Booking)
class AdminDestinationBooking(admin.ModelAdmin):
    list_display = ['name', 'contact', 'destination_name', 'depature', 'booking', 'status', 'handled_by']
    search_fields = ['name', 'email', 'contact', 'destination_name', 'depature']
    list_per_page = 20
    ordering = ['-depature']
    list_filter = ['status', 'booking']


@admin.register(Destination_Category)
class DestinationCategory(admin.ModelAdmin):
    list_display = ['name', 'status']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'status']


@admin.register(About)
class AdminAbout(admin.ModelAdmin):
    list_display = ['name', 'post', 'status', 'show_image']
    search_fields = ['name', 'status']
    list_per_page = 20

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Images'


@admin.register(Testimonial)
class AdminTestimonial(admin.ModelAdmin):
    list_display = ['name', 'status', 'show_image']
    search_fields = ['name', 'status']
    list_per_page = 20

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Images'


@admin.register(BlogData)
class AdminBlogz(admin.ModelAdmin):
    list_display = ['title', 'status', 'latest', 'created', 'show_image']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'status']
    list_per_page = 20
    ordering = ['-created']
    date_hierarchy = 'created'

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Images'


@admin.register(PopUp)
class AdminPopUp(admin.ModelAdmin):
    list_display = ['name', 'status', 'show_image']
    search_fields = ['name', 'status']

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Images'


@admin.register(Vacancy)
class AdminVacancy(admin.ModelAdmin):
    list_display = ['title', 'status']
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title', 'status']


@admin.register(ApplicantData)
class AdminApplicantData(admin.ModelAdmin):
    list_display = ['name', 'position', 'contact', 'applied_date', 'show_url', 'show_image']
    search_fields = ['name', 'email']
    date_hierarchy = 'applied_date'
    list_per_page = 20
    ordering = ['-applied_date']
    actions = ['export_xls', 'export_applicant_xls_all']

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.photo.url))

    show_image.short_description = 'Images'

    def show_url(self, object):
        return format_html('<a href="{}" width="50" height="50" target="_blank"> View Resume </a>',
                           format(object.cv.url))

    show_url.short_description = 'Resume'

    def export_xls(modeladmin, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Vacacy Applications.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("ApplicantData")

        row_num = 0

        columns = [
            (u"ID", 1000),
            (u"Name", 6000),
            (u"Email", 8000),
            (u"Contact", 8000),
            (u"Position", 8000),
            # (u"Applied Date", 8000),
        ]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        for obj in queryset:
            row_num += 1
            row = [
                obj.pk,
                obj.name,
                obj.email,
                obj.contact,
                obj.position,
                # obj.applied_date
            ]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    export_xls.short_description = "Export selected data"

    def export_applicant_xls_all(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Vacacy Applications.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("ApplicantData")

        row_num = 0

        columns = [
            (u"Name", 6000),
            (u"Email", 8000),
            (u"Contact", 8000),
            (u"Position", 8000),
            (u"Cv", 18000),
            (u"Photo", 18000),

        ]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1

        rows = ApplicantData.objects.all().values_list('name', 'email', 'contact', 'position', 'cv', 'photo')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    export_applicant_xls_all.short_description = 'Export all data at once'


@admin.register(NewsletterUser)
class AdminNewsletter(admin.ModelAdmin):
    list_display = ['email', 'date_added']
    search_fields = ['email', 'date_added']


@admin.register(Newsletter)
class AdminNewsletters(admin.ModelAdmin):
    list_display = ['subject', 'status', 'created', 'updated']
    search_fields = ['subject', 'email']
    actions = ['send_mail']


# ADMIN_PROFILE


class ProfileInline(admin.StackedInline):
    model = Admin_Profile
    can_delete = False
    verbose_name_plural = 'Admin Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location', 'get_image')
    list_display = ('username', 'is_staff')

    def get_location(self, instance):
        return instance.admin_profile.location

    get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ADMIN_PROFILE_END

@admin.register(Customer_Records)
class AdminCustomerRecord(admin.ModelAdmin):
    list_display = ['name', 'location', 'contact', 'show_image']
    search_fields = ['name', 'location', 'contact']

    class Meta:
        verbose_name_plural = 'Customer_Record'

    def show_image(self, object):
        return format_html('<img src="{}" width="100">', format(object.image.url))

    show_image.short_description = 'Images'
