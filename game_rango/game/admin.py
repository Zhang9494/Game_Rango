from django.contrib import admin
from game.models import Category, Game
from game.models import UserProfile

# Generate the slug field in admin page.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


# Register your models here.


admin.site.register(Category, CategoryAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(UserProfile)