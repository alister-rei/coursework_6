from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Client
from .forms import ClientForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': 'Clients list'
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:  # для работников и суперпользователя
            queryset = super().get_queryset()
        else:  # для остальных пользователей
            queryset = super().get_queryset().filter(owner=user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()
        context['title'] = client.email
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Add client'
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clients:view', args=[self.object.pk])


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    extra_context = {
        'title': 'Update client'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user or self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('clients:view', args=[self.object.pk])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    extra_context = {
        'title': 'Delete client'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user or self.request.user.is_staff:
            raise Http404
        return self.object
