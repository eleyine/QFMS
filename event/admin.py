from django.contrib import admin
from event.models.main import Event
import event
from event.models.page import Page, Section, SECTION_CLASSES, PerkItem, WorkshopItem, TalkItem, SponsorItem
from event.models.assets import Person, Company, Prize, PrizePerk, Place, Address, SocialMediaAccount


class CustomStackedInline(admin.StackedInline):
    extra = 0

section_class_inlines = []
for section_class in SECTION_CLASSES:
    section_class_inline = type(str(section_class), (CustomStackedInline,), {
        'extra': 0,
        'model': section_class})
    section_class_inlines.append(section_class_inline)

class PageAdmin(admin.ModelAdmin):
    inlines = section_class_inlines

class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'
    fieldsets = (
        ('General Info', {
            'fields': (
                ('first_name', 'last_name'),
                'category',
                'company',
                'gender', 
                'rank',
                )
        }),
        ('About', {
            'fields': (
                'profile_pic',
                'role',
                'biography',
                )
        }),
        ('Contact Info', {
            'fields': (
                'email',
                'telephone',
                )
        }),
        ('Social Media', {
            'fields': (
                'linkedin',
                'website',
                'twitter',
                'github',
                'facebook',
                )
        }),
        )
    list_display = (
            'updated_at',
            'category',
            'rank',
            'profile_pic',
            'full_name',
            'company',
            'role',
            'email', 
            'has_telephone',
            'has_linkedin',
            'has_website',
            'has_twitter',
            'has_github',
            'has_facebook',           
        )
    # list_editable = ('staff_comments',)
    search_fields = ['category', 'company', 'email', 'first_name', 'last_name']
    list_filter = ('category', 'company', 'gender')
    list_display_links = ('full_name',)

admin.site.register(Event)
admin.site.register(Page, PageAdmin)
admin.site.register(PerkItem)
admin.site.register(WorkshopItem)
admin.site.register(TalkItem)
admin.site.register(Sponsor)

admin.site.register(SocialMediaAccount)

admin.site.register(Place)
admin.site.register(Address)
admin.site.register(Person, PersonAdmin)
admin.site.register(Company)
admin.site.register(Prize)
admin.site.register(PrizePerk)

