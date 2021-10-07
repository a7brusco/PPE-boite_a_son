from django.shortcuts import get_object_or_404
from django.views import generic, View
from django.views.generic import edit
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.utils import timezone
from django.templatetags.static import static
from django.core import serializers
import json
from django.db.models import Q
from .models import Project
from .forms import ConfirmationForm, PasswordChangingForm
from django.template.loader import render_to_string
from django.core.files import File 

class ProjectListView(LoginRequiredMixin,generic.ListView):
    model = Project
    template_name = "samples/project_list.html"

    def get_queryset(self):
        q_objects=Q(user_id=self.request.user.id)
        queryset=super().get_queryset().filter(q_objects)
        return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProjectCreateView(LoginRequiredMixin,edit.CreateView):
    model = Project
    fields = ["name","typeOfMusic", "file"]
    success_url = reverse_lazy('projectList')
    
    def form_valid(self, form):
        print("sgdsfg")
        user = self.request.user
        form.instance.user = user
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)