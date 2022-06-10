from django.contrib import admin

from . import models

# i use this : allows us to utilize the admin interface and our Jango website with the ability to edit models on 
# --the same page as the parent model.So our group member basically has a bit of a parent model with group.
# And what we can do is we can use a tabular inline class so that when we visit the admin page I can click on
#  group and then see the group members and edit those as well.
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember



admin.site.register(models.Group)


 
