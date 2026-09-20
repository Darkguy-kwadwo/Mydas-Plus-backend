from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Agent, BlogPost, Property, PropertyImage, Testimonial


def format_ghs(amount):
    if amount is None:
        return '—'
    return f'GHS {amount:,.0f}'


def file_url(field):
    if not field:
        return None
    try:
        return field.url
    except ValueError:
        return None


class ListingStatusFilter(admin.SimpleListFilter):
    title = 'listing status'
    parameter_name = 'listing_status'

    def lookups(self, request, model_admin):
        return (
            ('sale', 'For sale'),
            ('rent', 'For rent'),
            ('both', 'Sale & rent'),
            ('featured', 'Featured only'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'sale':
            return queryset.filter(for_sale=True)
        if value == 'rent':
            return queryset.filter(for_rent=True)
        if value == 'both':
            return queryset.filter(for_sale=True, for_rent=True)
        if value == 'featured':
            return queryset.filter(featured=True)
        return queryset


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ('image', 'sort_order', 'thumb')
    readonly_fields = ('thumb',)
    ordering = ('sort_order', 'id')

    @admin.display(description='Preview')
    def thumb(self, obj):
        url = file_url(getattr(obj, 'image', None))
        if not url:
            return '—'
        return format_html(
            '<img src="{}" alt="" style="width:64px;height:48px;object-fit:cover;'
            'border-radius:6px;background:#f3f4f6;" />',
            url,
        )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'photo_thumb',
        'title',
        'type',
        'city',
        'price_display',
        'featured',
        'for_sale',
        'for_rent',
        'agent',
        'posted_date',
    )
    list_display_links = ('photo_thumb', 'title')
    list_editable = ('featured', 'for_sale', 'for_rent')
    list_filter = (ListingStatusFilter, 'type', 'city', 'agent', 'posted_date')
    search_fields = ('title', 'location', 'city', 'description', 'features')
    autocomplete_fields = ('agent',)
    date_hierarchy = 'posted_date'
    ordering = ('-posted_date', '-id')
    list_per_page = 25
    save_on_top = True
    readonly_fields = ('photo_preview',)
    inlines = [PropertyImageInline]

    fieldsets = (
        (
            'Listing basics',
            {
                'description': 'Title, type, and short description shown on the website.',
                'fields': ('title', 'type', 'description'),
            },
        ),
        (
            'Price & availability',
            {
                'description': 'Toggle sale/rent and mark featured to pin on the homepage.',
                'fields': (
                    ('price', 'rent_price'),
                    ('for_sale', 'for_rent', 'featured'),
                ),
            },
        ),
        (
            'Location',
            {
                'fields': ('location', 'city'),
            },
        ),
        (
            'Details',
            {
                'fields': (
                    ('bedrooms', 'bathrooms', 'area'),
                    'features',
                ),
                'description': 'For cars, use area as mileage or leave blank. Features is a list, e.g. ["Pool", "Garage"].',
            },
        ),
        (
            'Main photo',
            {
                'fields': ('photo_preview', 'image'),
                'description': 'Upload the main photo with Choose file. Add more photos in the Gallery section below.',
            },
        ),
        (
            'Agent & dates',
            {
                'fields': ('agent', 'posted_date'),
            },
        ),
    )

    @admin.display(description='Photo')
    def photo_thumb(self, obj):
        url = file_url(obj.image)
        if not url:
            return '—'
        return format_html(
            '<img src="{}" alt="" style="width:56px;height:42px;object-fit:cover;'
            'border-radius:6px;background:#f3f4f6;" />',
            url,
        )

    @admin.display(description='Price', ordering='price')
    def price_display(self, obj):
        sale = format_ghs(obj.price) if obj.for_sale else None
        rent = f'{format_ghs(obj.rent_price)}/mo' if obj.for_rent and obj.rent_price else None
        if sale and rent:
            return f'{sale} · {rent}'
        return sale or rent or format_ghs(obj.price)

    @admin.display(description='Current photo')
    def photo_preview(self, obj):
        url = file_url(getattr(obj, 'image', None))
        if not url:
            return mark_safe('<p style="color:#6b7280;">Upload a main photo below to see a preview.</p>')
        return format_html(
            '<img src="{}" alt="{}" style="max-width:320px;max-height:200px;object-fit:cover;'
            'border-radius:10px;border:1px solid #e5e7eb;" />',
            url,
            obj.title,
        )


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('photo_thumb', 'name', 'email', 'phone', 'rating', 'properties_count', 'listing_count')
    list_display_links = ('photo_thumb', 'name')
    search_fields = ('name', 'email', 'phone', 'bio')
    list_filter = ('rating',)
    ordering = ('name',)
    save_on_top = True
    readonly_fields = ('photo_preview', 'listing_count')

    fieldsets = (
        (
            'Profile',
            {
                'fields': ('name', 'bio', ('email', 'phone')),
            },
        ),
        (
            'Photo',
            {
                'fields': ('photo_preview', 'image'),
                'description': 'Click Choose file to upload a profile photo.',
            },
        ),
        (
            'Stats',
            {
                'fields': (('rating', 'properties_count'), 'listing_count'),
            },
        ),
    )

    @admin.display(description='Photo')
    def photo_thumb(self, obj):
        url = file_url(obj.image)
        if not url:
            return '—'
        return format_html(
            '<img src="{}" alt="" style="width:40px;height:40px;object-fit:cover;'
            'border-radius:999px;background:#f3f4f6;" />',
            url,
        )

    @admin.display(description='Current photo')
    def photo_preview(self, obj):
        url = file_url(getattr(obj, 'image', None))
        if not url:
            return mark_safe('<p style="color:#6b7280;">Upload a photo below to see a preview.</p>')
        return format_html(
            '<img src="{}" alt="{}" style="width:96px;height:96px;object-fit:cover;'
            'border-radius:999px;border:1px solid #e5e7eb;" />',
            url,
            obj.name,
        )

    @admin.display(description='Active listings')
    def listing_count(self, obj):
        return obj.listings.count()


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('photo_thumb', 'title', 'category', 'author', 'date')
    list_display_links = ('photo_thumb', 'title')
    list_filter = ('category', 'date')
    search_fields = ('title', 'excerpt', 'content', 'author')
    date_hierarchy = 'date'
    ordering = ('-date', '-id')
    save_on_top = True
    readonly_fields = ('photo_preview',)

    fieldsets = (
        (
            'Post',
            {
                'fields': ('title', 'category', ('author', 'date')),
            },
        ),
        (
            'Content',
            {
                'fields': ('excerpt', 'content'),
            },
        ),
        (
            'Cover image',
            {
                'fields': ('photo_preview', 'image'),
                'description': 'Click Choose file to upload a cover image.',
            },
        ),
    )

    @admin.display(description='Photo')
    def photo_thumb(self, obj):
        url = file_url(obj.image)
        if not url:
            return '—'
        return format_html(
            '<img src="{}" alt="" style="width:56px;height:42px;object-fit:cover;'
            'border-radius:6px;background:#f3f4f6;" />',
            url,
        )

    @admin.display(description='Current cover')
    def photo_preview(self, obj):
        url = file_url(getattr(obj, 'image', None))
        if not url:
            return mark_safe('<p style="color:#6b7280;">Upload a cover image below to see a preview.</p>')
        return format_html(
            '<img src="{}" alt="{}" style="max-width:320px;max-height:180px;object-fit:cover;'
            'border-radius:10px;border:1px solid #e5e7eb;" />',
            url,
            obj.title,
        )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('photo_thumb', 'name', 'role', 'rating', 'short_quote')
    list_display_links = ('photo_thumb', 'name')
    list_editable = ('rating',)
    search_fields = ('name', 'role', 'content')
    ordering = ('id',)
    save_on_top = True
    readonly_fields = ('photo_preview',)

    fieldsets = (
        (
            'Client',
            {
                'fields': (('name', 'role'), 'rating'),
            },
        ),
        (
            'Quote',
            {
                'fields': ('content',),
            },
        ),
        (
            'Photo',
            {
                'fields': ('photo_preview', 'image'),
                'description': 'Click Choose file to upload a photo.',
            },
        ),
    )

    @admin.display(description='Photo')
    def photo_thumb(self, obj):
        url = file_url(obj.image)
        if not url:
            return '—'
        return format_html(
            '<img src="{}" alt="" style="width:40px;height:40px;object-fit:cover;'
            'border-radius:999px;background:#f3f4f6;" />',
            url,
        )

    @admin.display(description='Quote')
    def short_quote(self, obj):
        text = (obj.content or '').strip()
        return text[:80] + ('…' if len(text) > 80 else '')

    @admin.display(description='Current photo')
    def photo_preview(self, obj):
        url = file_url(getattr(obj, 'image', None))
        if not url:
            return mark_safe('<p style="color:#6b7280;">Upload a photo below to see a preview.</p>')
        return format_html(
            '<img src="{}" alt="{}" style="width:80px;height:80px;object-fit:cover;'
            'border-radius:999px;border:1px solid #e5e7eb;" />',
            url,
            obj.name,
        )


admin.site.site_header = 'Mydas Plus Admin'
admin.site.site_title = 'Mydas Plus'
admin.site.index_title = 'Manage your listings'
admin.site.enable_nav_sidebar = True
