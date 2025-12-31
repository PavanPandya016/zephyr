from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Zeph

class ZephListView(LoginRequiredMixin, ListView):
    model = Zeph
    template_name = "posts/feed.html"
    context_object_name = "zephs"
    paginate_by = 20

class ZephDetailView(LoginRequiredMixin, DetailView):
    model = Zeph
    template_name = "posts/detail.html"

class ZephCreatView(LoginRequiredMixin, CreateView):
    model = Zeph
    fields = ["content", "image", "parent"]
    template_name = "posts/create.html"
    success_url = reverse_lazy("post:feed")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class ZephUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zeph
    fields = ["content", "image"]
    template_name = "posts/edit.html"

    def test_func(self):
        return self.get_object().author == self.request.user
    
class ZephDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Zeph
    template_name = "posts/delete.html"
    success_url = reverse_lazy("post:feed")

    def test_func(self):
        return super().get_object().author == self.request.user
    
