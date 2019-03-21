from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    amount = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Game(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128, unique=True)
    publisher = models.CharField(max_length=128)
    url = models.URLField()
    mark = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    picture = models.ImageField(upload_to='game_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


#class Comment(models.Model):
#    user = models.ForeignKey(UserProfile)
#    game = models.ForeignKey(Game)
#    date = models.DateField(auto_now=True)
#    content = models.CharField(max_length=128)

#    def __str__(self):
#        return self.content

