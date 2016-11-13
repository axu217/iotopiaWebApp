from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import UserForm
from . import services

class UserFormView(View):
	form_class = UserForm
	template_name = 'login/index.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			result = services.login(username, password, request)

			if result == "success":
				return redirect('main:index')
		return render(request, self.template_name, {'form': form})

