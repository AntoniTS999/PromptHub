from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from prompts.models import Category, Author, Prompt, Rating, Comment

admin.site.unregister(Group)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]



@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("display_name",)
    search_fields = UserAdmin.search_fields + ("display_name",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("display_name",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("display_name",)}),)

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_at",]
    search_fields = ["title", "categories__name"]
    list_filter = ["author", "created_at", "categories"]


class RatingAdmin(admin.ModelAdmin):
    list_display = ["value"]
admin.site.register(Rating, RatingAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user","content", "prompt__title"]
    list_filter = ["user", "created_at", "content"]
