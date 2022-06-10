from django.db import models
#just allows to remove any characters that alpha numeric or underscores 
# the behind idea for use that : if you have a string that has spaces in it and you want to use that as part of url it's
# -- going to be able to lowercase and add dashes instead of spaces 
from django.utils.text import slugify
#

import misaka
from django.urls import reverse
from django.contrib.auth import get_user_model
User=get_user_model()
# use this to custom template tags 
# using that to allow to call the group and user in Groupmember with their related name
from django import template
register=template.Library()

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through="GroupMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)


# Create your models here.
