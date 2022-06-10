from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
#A simple mixin which allows you to specify a list or tuple of foreign key fields to perform a select_related on.
from braces.views import SelectRelatedMixin

from . import forms
from . import models
from .models import Group

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    # I'm also going to have this method or attribute selected underscore related, 
    # which is just the mixin that allows us to provide a tuple related model.So basically
    #  the foreign keys for this post and that's going to be the user that the post belongs
    #  to and the group that the post belongs to.
    select_related = ("user", "group")
    queryset=models.Post.objects.all()
    # ??????????
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
        context['all_groups'] = Group.objects.all()
        return context


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"
    #You use prefetch_related when you're going to get a "set" of things, 
    # so ManyToManyFields as you stated or reverse ForeignKey

     # iexact: Case-insensitive exact match. If the value provided for comparison is None,
            #  it will be interpreted as an SQL NULL
    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
    # ????????
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")
    """
    Return the `QuerySet` that will be used to look up the object.
    This method is called by the default implementation of get_object() and
    may not be called if get_object() is overridden.
    """
    def get_queryset(self):
        """
        super().get_queryset() calls the get_queryset() method of its parent class and if multiple parents
         then it follows MRO to determine which class method to call
         and what will happen in the absence of this line -> the function get_queryset() will
          not be inherited from parent class, only the newly written function will be execuded
        """
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    #And essentially what this is, it's just to connect the actual post to the user itself.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    # using this to view what will happend after delete
    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

