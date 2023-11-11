from django.contrib import admin
from blog.models import Post,Category,Comment
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    list_display = ('title','author', 'counted_views', 'status',
                    'published_date', 'created_date')
    list_filter = ('status','author')
    search_fields = ['title', 'content']
    summernote_fields = ('content',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'post', 'approved', 'created_date', 'updated_date')
    list_filter = ('approved', 'created_date', 'updated_date')
    search_fields = ('name', 'subject', 'message')
    list_editable = ('approved',)
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = (
        ('Comment Details', {
            'fields': ('name', 'email', 'subject', 'message', 'post'),  # Include 'post' in the fields
            'classes': ('wide',),
        }),
        ('Approval', {
            'fields': ('approved',),
        }),
        ('Dates', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse', 'wide'),
        }),
    )

    # Customize the display name for the 'post' field
    def post(self, obj):
        return obj.post.title
    post.short_description = 'Post Title'

    # Override the 'save_model' method to automatically set the author
    def save_model(self, request, obj, form, change):
        if not obj.post:
            # Set a default post (e.g., General post) when no post is specified
            obj.post = Post.objects.get_or_create(title="General")[0]
        super().save_model(request, obj, form, change)



admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
